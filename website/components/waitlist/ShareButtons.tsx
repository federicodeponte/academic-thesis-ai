'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Check, Copy, Mail, Linkedin } from 'lucide-react';
import { FaXTwitter } from 'react-icons/fa6';

interface ShareButtonsProps {
  referralLink: string;
  referralCode: string;
}

export function ShareButtons({ referralLink, referralCode }: ShareButtonsProps) {
  const [copied, setCopied] = useState(false);

  const shareText = `Join me on the OpenDraft waitlist! Get a free AI-generated thesis. Use my referral code: ${referralCode}`;

  const handleCopy = async () => {
    await navigator.clipboard.writeText(referralLink);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleTwitterShare = () => {
    const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareText)}&url=${encodeURIComponent(referralLink)}`;
    window.open(url, '_blank', 'width=550,height=420');
  };

  const handleLinkedInShare = () => {
    const url = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(referralLink)}`;
    window.open(url, '_blank', 'width=550,height=420');
  };

  const handleEmailShare = () => {
    const subject = 'Join me on OpenDraft waitlist';
    const body = `Hey!\n\nI just joined the OpenDraft waitlist to get a free AI-generated thesis. You should join too!\n\nUse my referral link:\n${referralLink}\n\nWe both get priority access when you verify your email!`;
    window.location.href = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  };

  return (
    <div className="space-y-3">
      {/* Copy link */}
      <div className="flex gap-2">
        <Input value={referralLink} readOnly className="flex-1 font-mono text-sm" />
        <Button onClick={handleCopy} variant="outline" size="icon">
          {copied ? (
            <Check className="h-4 w-4 text-green-500" />
          ) : (
            <Copy className="h-4 w-4" />
          )}
        </Button>
      </div>

      {/* Social share buttons */}
      <div className="grid grid-cols-3 gap-2">
        <Button
          onClick={handleTwitterShare}
          variant="outline"
          className="flex items-center gap-2"
          size="sm"
        >
          <FaXTwitter className="h-4 w-4" />
          <span className="hidden sm:inline">Twitter</span>
        </Button>

        <Button
          onClick={handleLinkedInShare}
          variant="outline"
          className="flex items-center gap-2"
          size="sm"
        >
          <Linkedin className="h-4 w-4" />
          <span className="hidden sm:inline">LinkedIn</span>
        </Button>

        <Button
          onClick={handleEmailShare}
          variant="outline"
          className="flex items-center gap-2"
          size="sm"
        >
          <Mail className="h-4 w-4" />
          <span className="hidden sm:inline">Email</span>
        </Button>
      </div>
    </div>
  );
}
