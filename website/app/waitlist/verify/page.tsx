import { CheckCircle, XCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

export const metadata = {
  title: 'Email Verification - OpenDraft Waitlist',
};

interface PageProps {
  searchParams: { error?: string };
}

export default function VerifyPage({ searchParams }: PageProps) {
  const hasError = searchParams.error;

  if (hasError) {
    return (
      <section className="container py-24 sm:py-32">
        <div className="max-w-2xl mx-auto text-center">
          <div className="bg-red-50 dark:bg-red-950 p-8 rounded-xl border-2 border-red-200 dark:border-red-800">
            <XCircle className="h-16 w-16 text-red-600 dark:text-red-400 mx-auto mb-4" />
            <h1 className="text-3xl font-bold text-red-800 dark:text-red-200 mb-4">
              Verification Failed
            </h1>
            <p className="text-red-700 dark:text-red-300 mb-6">
              {searchParams.error || 'Invalid or expired verification link.'}
            </p>
            <Button asChild>
              <Link href="/waitlist">Back to Waitlist</Link>
            </Button>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="container py-24 sm:py-32">
      <div className="max-w-2xl mx-auto text-center">
        <div className="bg-green-50 dark:bg-green-950 p-8 rounded-xl border-2 border-green-200 dark:border-green-800">
          <CheckCircle className="h-16 w-16 text-green-600 dark:text-green-400 mx-auto mb-4" />
          <h1 className="text-3xl font-bold text-green-800 dark:text-green-200 mb-4">
            Email Verified!
          </h1>
          <p className="text-green-700 dark:text-green-300 mb-6">
            Your email has been successfully verified. You&apos;re now in the waitlist queue!
          </p>
          <p className="text-sm text-green-600 dark:text-green-400 mb-8">
            Check your dashboard to see your position and referral link.
          </p>
          <Button asChild className="bg-green-600 hover:bg-green-700 text-white">
            <Link href="/waitlist">View Dashboard</Link>
          </Button>
        </div>
      </div>
    </section>
  );
}
