import {
  Body,
  Button,
  Container,
  Head,
  Heading,
  Html,
  Preview,
  Section,
  Text,
} from '@react-email/components';
import * as React from 'react';

interface ReferralRewardEmailProps {
  fullName: string;
  newPosition: number;
  oldPosition: number;
  referralCount: number;
  dashboardUrl: string;
}

export const ReferralRewardEmail = ({
  fullName = 'Student',
  newPosition = 50,
  oldPosition = 150,
  referralCount = 3,
  dashboardUrl = 'https://opendraft.ai/waitlist/abc123',
}: ReferralRewardEmailProps) => (
  <Html>
    <Head />
    <Preview>You skipped 100 positions on the waitlist! 🎉</Preview>
    <Body style={main}>
      <Container style={container}>
        <Heading style={h1}>Congratulations, {fullName}! 🎉</Heading>

        <Section style={celebrationBox}>
          <Text style={bigText}>
            You just skipped <strong>100 positions</strong>!
          </Text>
          <Text style={text}>
            <span style={strikethrough}>#{oldPosition}</span> → <span style={highlight}>#{newPosition}</span>
          </Text>
        </Section>

        <Text style={text}>
          Thanks to your <strong>{referralCount} verified referrals</strong>, you've moved up the waitlist significantly!
        </Text>

        <Section style={infoBox}>
          <Text style={infoTitle}>Keep Going! 🚀</Text>
          <Text style={smallText}>
            Every 3 verified referrals earns you another 100-position skip. Share your link with more friends to move even faster!
          </Text>
        </Section>

        <Section style={buttonContainer}>
          <Button style={button} href={dashboardUrl}>
            View Dashboard
          </Button>
        </Section>

        <Section style={tipsBox}>
          <Text style={tipsTitle}>Referral Tips:</Text>
          <ul style={list}>
            <li>Share on social media (Twitter, LinkedIn)</li>
            <li>Email your classmates or study group</li>
            <li>Post in academic Discord/Slack channels</li>
            <li>Share in your university's Facebook group</li>
          </ul>
          <Text style={smallText}>
            Remember: Only <strong>verified referrals</strong> count. Make sure your friends verify their email!
          </Text>
        </Section>

        <Text style={footer}>
          Thanks for spreading the word!
          <br />
          OpenDraft Team
        </Text>
      </Container>
    </Body>
  </Html>
);

export default ReferralRewardEmail;

const main = {
  backgroundColor: '#f6f9fc',
  fontFamily: '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Ubuntu,sans-serif',
};

const container = {
  backgroundColor: '#ffffff',
  margin: '0 auto',
  padding: '20px 0 48px',
  marginBottom: '64px',
  maxWidth: '600px',
};

const h1 = {
  color: '#26251e',
  fontSize: '24px',
  fontWeight: 'bold',
  margin: '40px 0',
  padding: '0 40px',
  textAlign: 'center' as const,
};

const text = {
  color: '#4b5563',
  fontSize: '16px',
  lineHeight: '24px',
  margin: '16px 0',
  padding: '0 40px',
  textAlign: 'center' as const,
};

const bigText = {
  color: '#26251e',
  fontSize: '20px',
  fontWeight: 'bold',
  lineHeight: '28px',
  margin: '0',
  textAlign: 'center' as const,
};

const celebrationBox = {
  backgroundColor: '#f0fdf4',
  borderRadius: '8px',
  margin: '24px 40px',
  padding: '24px',
  border: '2px solid #22c55e',
};

const strikethrough = {
  textDecoration: 'line-through',
  color: '#9ca3af',
  fontSize: '18px',
};

const highlight = {
  color: '#22c55e',
  fontSize: '28px',
  fontWeight: 'bold',
};

const infoBox = {
  backgroundColor: '#ede9fe',
  borderRadius: '8px',
  margin: '24px 40px',
  padding: '16px',
  border: '1px solid #8B5CF6',
};

const infoTitle = {
  color: '#26251e',
  fontSize: '16px',
  fontWeight: 'bold',
  margin: '0 0 8px 0',
};

const tipsBox = {
  backgroundColor: '#f9fafb',
  borderRadius: '8px',
  margin: '24px 40px',
  padding: '16px',
};

const tipsTitle = {
  color: '#26251e',
  fontSize: '16px',
  fontWeight: 'bold',
  margin: '0 0 12px 0',
};

const smallText = {
  color: '#4b5563',
  fontSize: '14px',
  lineHeight: '20px',
  margin: '8px 0',
};

const list = {
  color: '#4b5563',
  fontSize: '14px',
  lineHeight: '20px',
  margin: '8px 0',
  paddingLeft: '20px',
};

const buttonContainer = {
  padding: '27px 40px',
  textAlign: 'center' as const,
};

const button = {
  backgroundColor: '#8B5CF6',
  borderRadius: '8px',
  color: '#fff',
  fontSize: '16px',
  fontWeight: 'bold',
  textDecoration: 'none',
  textAlign: 'center' as const,
  display: 'inline-block',
  padding: '12px 24px',
};

const footer = {
  color: '#6b7280',
  fontSize: '14px',
  lineHeight: '24px',
  margin: '32px 0',
  padding: '0 40px',
  textAlign: 'center' as const,
};
