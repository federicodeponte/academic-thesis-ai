#!/usr/bin/env python3
"""
ABOUTME: Streamlit web UI for Academic Thesis AI
ABOUTME: Provides browser-based interface for markdown editing and PDF generation
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.pdf_engines import (
    PDFEngineFactory,
    PDFGenerationOptions,
    get_available_engines,
    get_recommended_engine
)

# Page config
st.set_page_config(
    page_title="Academic Thesis AI",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("📚 Academic Thesis AI")
st.markdown("**AI-Powered Academic Writing Framework** - From literature review to publication-ready papers")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")

    # PDF Engine selection
    available_engines = get_available_engines()
    recommended = get_recommended_engine()

    st.subheader("PDF Generation")
    engine_options = ['Auto (Recommended)'] + available_engines
    selected_engine = st.selectbox(
        "Engine",
        engine_options,
        help=f"Recommended: {recommended}"
    )

    # PDF Options
    with st.expander("PDF Options"):
        font_size = st.selectbox("Font Size", ["10pt", "11pt", "12pt"], index=2)
        line_spacing = st.slider("Line Spacing", 1.0, 2.5, 2.0, 0.1)
        margins = st.selectbox("Margins", ["0.75in", "1in", "1.25in"], index=1)
        page_numbers = st.checkbox("Page Numbers", value=True)

    # Title page options
    with st.expander("Title Page (Optional)"):
        include_title_page = st.checkbox("Include Title Page")
        if include_title_page:
            title = st.text_input("Paper Title")
            author = st.text_input("Author Name")
            institution = st.text_input("Institution")
            course = st.text_input("Course Code")
            instructor = st.text_input("Instructor")

    # Table of Contents
    enable_toc = st.checkbox("Table of Contents", value=False)
    if enable_toc:
        toc_depth = st.slider("TOC Depth", 1, 4, 2)

    st.divider()
    st.caption(f"Available engines: {len(available_engines)}")
    st.caption(f"Recommended: {recommended}")

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["✍️ Editor", "📄 Templates", "📚 Agents", "ℹ️ About"])

with tab1:
    st.header("Markdown Editor")

    # File upload or new document
    col1, col2 = st.columns([3, 1])
    with col1:
        uploaded_file = st.file_uploader("Upload existing markdown file", type=['md', 'markdown'])
    with col2:
        st.metric("Characters", len(st.session_state.get('markdown_content', '')))

    # Markdown editor
    if uploaded_file:
        markdown_content = uploaded_file.read().decode('utf-8')
    else:
        markdown_content = st.session_state.get('markdown_content', '''# My Academic Paper

**Author:** Your Name

---

## Abstract

[Write your abstract here]

---

## 1. Introduction

[Write your introduction here]

''')

    # Text area for editing
    edited_content = st.text_area(
        "Edit your markdown",
        value=markdown_content,
        height=400,
        help="Write your paper in markdown format"
    )

    # Save to session state
    st.session_state['markdown_content'] = edited_content

    # Action buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💾 Download Markdown", use_container_width=True):
            st.download_button(
                label="⬇️ Download .md",
                data=edited_content,
                file_name="paper.md",
                mime="text/markdown"
            )

    with col2:
        if st.button("📄 Generate PDF", type="primary", use_container_width=True):
            with st.spinner("Generating PDF..."):
                try:
                    # Save markdown to temp file
                    temp_md = Path("temp_paper.md")
                    temp_md.write_text(edited_content)

                    # Create PDF options
                    options = PDFGenerationOptions(
                        font_size=font_size,
                        line_spacing=line_spacing,
                        margins=margins,
                        page_numbers=page_numbers
                    )

                    # Add title page if enabled
                    if include_title_page and title:
                        options.title = title
                        options.author = author
                        options.institution = institution
                        options.course = course
                        options.instructor = instructor

                    # Add TOC if enabled
                    if enable_toc:
                        options.enable_toc = True
                        options.toc_depth = toc_depth

                    # Generate PDF
                    temp_pdf = Path("temp_paper.pdf")
                    engine_name = None if selected_engine == 'Auto (Recommended)' else selected_engine.lower().replace('/', '')

                    result = PDFEngineFactory.generate_with_fallback(
                        md_file=temp_md,
                        output_pdf=temp_pdf,
                        options=options,
                        preferred_engine=engine_name
                    )

                    if result.success:
                        st.success(f"✅ PDF generated successfully using {result.engine_name}!")

                        # Provide download button
                        with open(temp_pdf, 'rb') as f:
                            st.download_button(
                                label="⬇️ Download PDF",
                                data=f,
                                file_name="paper.pdf",
                                mime="application/pdf"
                            )

                        # Clean up
                        temp_md.unlink(missing_ok=True)
                        temp_pdf.unlink(missing_ok=True)
                    else:
                        st.error(f"❌ PDF generation failed: {result.error_message}")
                        temp_md.unlink(missing_ok=True)

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    with col3:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state['markdown_content'] = ''
            st.rerun()

with tab2:
    st.header("📄 Quick-Start Templates")

    st.markdown("""
    Choose a template to get started quickly:
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📚 Literature Review")
        st.markdown("Systematic review of 20-50 papers")
        if st.button("Load Template", key="lit_review"):
            try:
                template_path = Path("examples/templates/literature_review.md")
                if template_path.exists():
                    st.session_state['markdown_content'] = template_path.read_text()
                    st.success("✅ Template loaded!")
                    st.rerun()
                else:
                    st.error("Template file not found")
            except Exception as e:
                st.error(f"Error: {e}")

    with col2:
        st.subheader("🔬 Empirical Study")
        st.markdown("IMRaD format research paper")
        if st.button("Load Template", key="empirical"):
            try:
                template_path = Path("examples/templates/empirical_study.md")
                if template_path.exists():
                    st.session_state['markdown_content'] = template_path.read_text()
                    st.success("✅ Template loaded!")
                    st.rerun()
                else:
                    st.error("Template file not found")
            except Exception as e:
                st.error(f"Error: {e}")

    with col3:
        st.subheader("💡 Theoretical Paper")
        st.markdown("Framework or theory development")
        if st.button("Load Template", key="theoretical"):
            try:
                template_path = Path("examples/templates/theoretical_paper.md")
                if template_path.exists():
                    st.session_state['markdown_content'] = template_path.read_text()
                    st.success("✅ Template loaded!")
                    st.rerun()
                else:
                    st.error("Template file not found")
            except Exception as e:
                st.error(f"Error: {e}")

with tab3:
    st.header("📚 AI Agents")

    st.markdown("""
    Academic Thesis AI includes 14 specialized agents to help you write:
    """)

    # Research Phase
    with st.expander("🔍 Phase 1: Research"):
        st.markdown("""
        - **Scout Agent** - Find 20-50 relevant papers
        - **Scribe Agent** - Deep paper summarization
        - **Signal Agent** - Research gap analysis
        """)
        st.info("💡 Use these agents in your IDE (Cursor/Claude Code)")

    # Structure Phase
    with st.expander("🏗️ Phase 2: Structure"):
        st.markdown("""
        - **Architect Agent** - Design paper outline
        - **Formatter Agent** - Apply academic styles (IMRaD, APA, IEEE)
        """)

    # Compose Phase
    with st.expander("✍️ Phase 3: Compose"):
        st.markdown("""
        - **Crafter Agent** - Write sections with citations
        - **Thread Agent** - Check consistency
        - **Narrator Agent** - Unify voice and tone
        """)

    # Validate Phase
    with st.expander("✅ Phase 4: Validate"):
        st.markdown("""
        - **Skeptic Agent** - Critical peer review
        - **Verifier Agent** - Fact-check citations
        - **Referee Agent** - Simulate journal review
        """)

    # Refine Phase
    with st.expander("✨ Phase 5: Refine"):
        st.markdown("""
        - **Voice Agent** - Match your writing style
        - **Entropy Agent** - Humanize text (anti-AI detection)
        - **Polish Agent** - Final grammar and flow
        """)

    st.markdown("---")
    st.markdown("**📁 Find all agent prompts in:** `prompts/` directory")
    st.markdown("**📖 See complete workflow:** `prompts/00_WORKFLOW.md`")

with tab4:
    st.header("ℹ️ About Academic Thesis AI")

    st.markdown("""
    ### 🎯 What is This?

    A **prompt-driven framework** for academic writing that uses specialized AI agents to assist with:
    - 📚 **Deep research** - Find and analyze 20-50 papers automatically
    - 🏗️ **Structure design** - Create publication-ready outlines
    - ✍️ **Section writing** - Draft with proper citations and flow
    - ✅ **Quality assurance** - Validate, fact-check, and peer-review simulate
    - 🎨 **Style refinement** - Polish and humanize your writing

    ### ✨ Key Features

    - **Zero-code setup** - Just prompts in your IDE
    - **14 specialized AI agents** - Each with specific expertise
    - **Real academic integration** - arXiv, Semantic Scholar, PubMed, Google Scholar
    - **Multi-LLM support** - Claude, GPT, Gemini
    - **Export to PDF/Word/LaTeX** - Publication-ready output
    - **100% tested** - All agents validated

    ### 🔒 Ethics & Responsible Use

    **Important principles:**
    1. **You are the author** - AI assists, doesn't replace
    2. **Verify everything** - Check all claims and citations
    3. **Disclose AI use** - Follow your institution's policies
    4. **Maintain integrity** - No plagiarism, no fabrication

    See `ETHICS.md` for comprehensive guidelines.

    ### 📊 Project Stats

    - **Lines of Code:** ~5,000+
    - **Agent Prompts:** 14 (all tested ✅)
    - **MCP Servers:** 4
    - **Supported Formats:** PDF, Word, LaTeX
    - **Test Coverage:** 100% (14/14 agents + 3/3 utilities)
    - **Status:** ✅ Production Ready

    ### 📚 Resources

    - **Documentation:** `README.md`
    - **Tutorial:** `examples/tutorial/README.md`
    - **Templates:** `examples/templates/`
    - **Ethics Guide:** `ETHICS.md`
    - **Docker Guide:** `docs/DOCKER.md`

    ### 🙏 Built With

    - Model Context Protocol (MCP) - Anthropic
    - arXiv MCP Server - @blazickjp
    - Semantic Scholar - Allen Institute for AI
    - Claude / GPT / Gemini - AI model providers

    ---

    **v1.1.0** | MIT License | Built with ❤️ for researchers
    """)

# Footer
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.caption("📚 Academic Thesis AI v1.1.0")
with col2:
    st.caption(f"🔧 Engines: {', '.join(available_engines)}")
with col3:
    st.caption("✅ Production Ready")
