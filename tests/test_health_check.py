#!/usr/bin/env python3
"""
ABOUTME: Unit tests for system health check in utils/health_check.py
ABOUTME: Tests API key detection, dependency checks, PDF engines, and system resources
"""

import pytest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from utils.health_check import (
    HealthChecker,
    HealthCheckResult
)


class TestHealthCheckResult:
    """Test HealthCheckResult dataclass."""

    def test_is_healthy(self):
        """Test healthy status detection."""
        result = HealthCheckResult(
            component="Test",
            status="healthy",
            message="OK"
        )
        assert result.is_healthy()
        assert not result.is_degraded()
        assert not result.is_failed()

    def test_is_degraded(self):
        """Test degraded status detection."""
        result = HealthCheckResult(
            component="Test",
            status="degraded",
            message="Warning"
        )
        assert result.is_degraded()
        assert not result.is_healthy()
        assert not result.is_failed()

    def test_is_failed(self):
        """Test failed status detection."""
        result = HealthCheckResult(
            component="Test",
            status="failed",
            message="Error"
        )
        assert result.is_failed()
        assert not result.is_healthy()
        assert not result.is_degraded()


class TestGeminiAPIKeyCheck:
    """Test Gemini API key detection."""

    @patch('config.get_config')
    def test_api_key_configured(self, mock_get_config):
        """Test API key is correctly detected when configured."""
        mock_config = MagicMock()
        mock_config.google_api_key = "AIza" + "x" * 35  # Valid format
        mock_get_config.return_value = mock_config

        checker = HealthChecker(verbose=False)
        result = checker.check_gemini_api_key()

        assert result.is_healthy()
        assert "configured" in result.message.lower()
        assert result.details["configured"] is True

    @patch('config.get_config')
    def test_api_key_missing(self, mock_get_config):
        """Test detection when API key is not set."""
        mock_config = MagicMock()
        mock_config.google_api_key = ""  # Empty string
        mock_get_config.return_value = mock_config

        checker = HealthChecker(verbose=False)
        result = checker.check_gemini_api_key()

        assert result.is_failed()
        assert "not configured" in result.message.lower()
        assert result.details["configured"] is False
        assert result.error is not None

    @patch('config.get_config')
    def test_api_key_suspicious_format(self, mock_get_config):
        """Test warning for API keys with unusual format."""
        mock_config = MagicMock()
        mock_config.google_api_key = "xyz123invalid"  # Doesn't start with AIza
        mock_get_config.return_value = mock_config

        checker = HealthChecker(verbose=False)
        result = checker.check_gemini_api_key()

        assert result.is_degraded()
        assert "unusual" in result.message.lower() or "suspicious" in result.message.lower()

    @patch('config.get_config')
    def test_api_key_exception_handling(self, mock_get_config):
        """Test graceful error handling when config access fails."""
        mock_get_config.side_effect = Exception("Config load error")

        checker = HealthChecker(verbose=False)
        result = checker.check_gemini_api_key()

        assert result.is_failed()
        assert result.error is not None


class TestPythonDependencies:
    """Test Python dependency checks."""

    def test_all_dependencies_installed(self):
        """Test when all core dependencies are available."""
        checker = HealthChecker(verbose=False)
        result = checker.check_python_dependencies()

        # Should be healthy if running in dev environment
        if result.is_healthy():
            assert "installed" in result.message.lower()
            assert len(result.details["installed"]) > 0

    @patch('builtins.__import__')
    def test_missing_dependencies(self, mock_import):
        """Test detection of missing packages."""
        def import_side_effect(name, *args, **kwargs):
            if name == "yaml":
                raise ImportError(f"No module named '{name}'")
            return MagicMock()

        mock_import.side_effect = import_side_effect

        checker = HealthChecker(verbose=False)
        result = checker.check_python_dependencies()

        assert result.is_failed()
        assert "missing" in result.message.lower()
        assert "missing" in result.details


class TestPDFEngines:
    """Test PDF engine availability checks."""

    def test_pdf_engines_check_structure(self):
        """Test PDF engine check returns list of results."""
        checker = HealthChecker(verbose=False)
        results = checker.check_pdf_engines()

        assert isinstance(results, list)
        assert len(results) > 0  # At least overall status

    def test_at_least_one_engine_available(self):
        """Test that at least one PDF engine is typically available."""
        checker = HealthChecker(verbose=False)
        results = checker.check_pdf_engines()

        # Find overall status result
        overall = next((r for r in results if "Overall" in r.component), None)
        assert overall is not None

        # In dev environment, should have at least one engine
        # (WeasyPrint is in dependencies)
        if overall.is_healthy():
            assert len(overall.details.get("available_engines", [])) > 0

    @patch('shutil.which')
    @patch('builtins.__import__')
    def test_no_pdf_engines_available(self, mock_import, mock_which):
        """Test when no PDF engines are available."""
        mock_which.return_value = None  # LibreOffice, Pandoc not found
        mock_import.side_effect = ImportError  # WeasyPrint not installed

        checker = HealthChecker(verbose=False)
        results = checker.check_pdf_engines()

        # Find overall status
        overall = next((r for r in results if "Overall" in r.component), None)
        assert overall is not None
        assert overall.is_failed()


class TestDiskSpaceCheck:
    """Test disk space monitoring."""

    def test_disk_space_check_structure(self):
        """Test disk space check returns valid result."""
        checker = HealthChecker(verbose=False)
        result = checker.check_disk_space(min_gb=1.0)

        assert isinstance(result, HealthCheckResult)
        assert result.component == "Disk Space"

    def test_disk_space_details(self):
        """Test disk space check includes diagnostic details."""
        checker = HealthChecker(verbose=False)
        result = checker.check_disk_space(min_gb=0.1)  # Very low threshold

        if result.is_healthy():
            assert "free_gb" in result.details
            assert "total_gb" in result.details
            assert "used_percent" in result.details
            assert result.details["free_gb"] > 0
            assert result.details["total_gb"] > 0

    @patch('shutil.disk_usage')
    def test_disk_space_low(self, mock_disk_usage):
        """Test detection of low disk space."""
        # Mock low disk space (0.5 GB free)
        mock_stat = MagicMock()
        mock_stat.free = 0.5 * (1024 ** 3)  # 0.5 GB in bytes
        mock_stat.total = 100 * (1024 ** 3)  # 100 GB total
        mock_stat.used = mock_stat.total - mock_stat.free
        mock_disk_usage.return_value = mock_stat

        checker = HealthChecker(verbose=False)
        result = checker.check_disk_space(min_gb=1.0)  # Require 1 GB

        assert result.is_failed()
        assert "low" in result.message.lower()

    @patch('shutil.disk_usage')
    def test_disk_space_degraded(self, mock_disk_usage):
        """Test degraded status for marginal disk space."""
        # Mock 1.5 GB free (more than 1 GB min, but less than 2x min)
        mock_stat = MagicMock()
        mock_stat.free = 1.5 * (1024 ** 3)
        mock_stat.total = 100 * (1024 ** 3)
        mock_stat.used = mock_stat.total - mock_stat.free
        mock_disk_usage.return_value = mock_stat

        checker = HealthChecker(verbose=False)
        result = checker.check_disk_space(min_gb=1.0)

        assert result.is_degraded()


class TestMemoryCheck:
    """Test system memory monitoring."""

    def test_memory_check_structure(self):
        """Test memory check returns valid result."""
        checker = HealthChecker(verbose=False)
        result = checker.check_memory(min_mb=512.0)

        assert isinstance(result, HealthCheckResult)
        assert result.component == "System Memory"

    @patch('builtins.__import__')
    def test_memory_check_without_psutil(self, mock_import):
        """Test graceful degradation when psutil unavailable."""
        def import_side_effect(name, *args, **kwargs):
            if name == "psutil":
                raise ImportError("No module named 'psutil'")
            return MagicMock()

        mock_import.side_effect = import_side_effect

        checker = HealthChecker(verbose=False)
        result = checker.check_memory(min_mb=512.0)

        assert result.is_degraded()
        assert "psutil" in result.message.lower()

    @patch('psutil.virtual_memory')
    def test_memory_healthy(self, mock_memory):
        """Test healthy memory status."""
        # Mock 2 GB available
        mock_mem = MagicMock()
        mock_mem.available = 2 * (1024 ** 3)  # 2 GB in bytes
        mock_mem.total = 16 * (1024 ** 3)  # 16 GB total
        mock_mem.percent = 50.0
        mock_memory.return_value = mock_mem

        checker = HealthChecker(verbose=False)
        result = checker.check_memory(min_mb=512.0)

        assert result.is_healthy()
        assert result.details["free_mb"] > 512.0

    @patch('psutil.virtual_memory')
    def test_memory_low(self, mock_memory):
        """Test detection of low memory."""
        # Mock 256 MB available (below 512 MB threshold)
        mock_mem = MagicMock()
        mock_mem.available = 256 * (1024 ** 2)  # 256 MB in bytes
        mock_mem.total = 8 * (1024 ** 3)
        mock_mem.percent = 95.0
        mock_memory.return_value = mock_mem

        checker = HealthChecker(verbose=False)
        result = checker.check_memory(min_mb=512.0)

        assert result.is_failed()
        assert "low" in result.message.lower()


class TestFilePermissions:
    """Test file system permission checks."""

    def test_file_permissions_check_structure(self):
        """Test file permissions check returns valid result."""
        checker = HealthChecker(verbose=False)
        result = checker.check_file_permissions()

        assert isinstance(result, HealthCheckResult)
        assert result.component == "File Permissions"

    def test_directories_created(self):
        """Test required directories are created by health check."""
        checker = HealthChecker(verbose=False)
        result = checker.check_file_permissions()

        # Directories should exist after check
        assert Path("logs").exists()
        assert Path("output").exists()

    @patch('os.access')
    def test_permission_denied(self, mock_access):
        """Test detection of permission issues."""
        mock_access.return_value = False  # No write permission

        checker = HealthChecker(verbose=False)
        result = checker.check_file_permissions()

        assert result.is_failed()
        assert "permission" in result.message.lower()


class TestHealthCheckerIntegration:
    """Integration tests for complete health check."""

    def test_check_all_returns_results(self):
        """Test check_all returns list of results."""
        checker = HealthChecker(verbose=False)
        results = checker.check_all()

        assert isinstance(results, list)
        assert len(results) > 0

    def test_check_all_covers_all_components(self):
        """Test check_all includes all health components."""
        checker = HealthChecker(verbose=False)
        results = checker.check_all()

        components = [r.component for r in results]

        # Required components
        assert any("API Key" in c for c in components)
        assert any("Dependencies" in c for c in components)
        assert any("Disk Space" in c for c in components)
        assert any("Memory" in c for c in components)
        assert any("Permission" in c for c in components)

    def test_results_have_status(self):
        """Test all results have valid status."""
        checker = HealthChecker(verbose=False)
        results = checker.check_all()

        valid_statuses = {"healthy", "degraded", "failed"}
        for result in results:
            assert result.status in valid_statuses

    def test_verbose_mode(self):
        """Test health checker can run in verbose mode."""
        # Should not raise exception
        checker = HealthChecker(verbose=True)
        results = checker.check_all()
        assert len(results) > 0

    def test_quiet_mode(self):
        """Test health checker can run in quiet mode."""
        checker = HealthChecker(verbose=False)
        results = checker.check_all()
        assert len(results) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
