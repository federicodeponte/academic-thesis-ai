import { redirect } from 'next/navigation';
import { supabaseAdmin } from '@/lib/supabase/admin';
import { Gift } from 'lucide-react';

interface PageProps {
  params: { code: string };
}

export default async function ReferralLandingPage({ params }: PageProps) {
  const { code } = params;

  // Verify referral code exists
  const { data: referrer } = await supabaseAdmin
    .from('waitlist')
    .select('full_name, position')
    .eq('referral_code', code)
    .single();

  // Redirect to waitlist signup with referral code
  redirect(`/waitlist?ref=${code}`);
}

export async function generateMetadata({ params }: PageProps) {
  const { code } = params;

  const { data: referrer } = await supabaseAdmin
    .from('waitlist')
    .select('full_name')
    .eq('referral_code', code)
    .single();

  const referrerName = referrer?.full_name || 'A friend';

  return {
    title: `${referrerName} invited you to OpenDraft Waitlist`,
    description: `Join ${referrerName} on the OpenDraft waitlist and get a free AI-generated thesis. Both of you get priority access!`,
  };
}
