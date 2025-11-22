// ABOUTME: Hero section - first impression with headline, CTAs, and visual branding
// ABOUTME: Shows dynamic GitHub stars badge, academic honesty alert, and real thesis screenshot carousel

"use client";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Carousel, CarouselContent, CarouselItem, CarouselNext, CarouselPrevious } from "@/components/ui/carousel";
import { AlertTriangle, ArrowRight, Github, Star } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { useGitHubStats, formatNumber } from "@/lib/hooks/useGitHubStats";

const CAROUSEL_ITEMS = [
  { src: "/examples/thesis_page_01.png", alt: "Thesis title page" },
  { src: "/examples/thesis_page_02.png", alt: "Abstract and table of contents" },
  { src: "/examples/thesis_page_03.png", alt: "Introduction chapter" },
  { src: "/examples/thesis_page_04.png", alt: "Literature review section" },
  { src: "/examples/thesis_page_05.png", alt: "Methodology chapter" },
];

export const HeroSection = () => {
  const { data: githubStats, loading: githubLoading } = useGitHubStats("federicodeponte/opendraft");

  return (
    <section className="container w-full">
      <div className="grid place-items-center lg:max-w-screen-xl gap-8 mx-auto py-20 md:py-32">
        <div className="text-center space-y-6">
          <div className="max-w-screen-md mx-auto text-center space-y-4">
            <h1 className="text-5xl md:text-7xl font-bold tracking-tight leading-[1.1] max-w-4xl mx-auto">
              Write Your Thesis{" "}
              <span className="bg-gradient-to-r from-brand-purple-500 to-brand-cyan-500 bg-clip-text text-transparent">
                10x Faster
              </span>{" "}
              with AI
            </h1>

            <p className="text-xl md:text-2xl text-muted-foreground font-medium max-w-2xl mx-auto mt-6">
              Generate a 20,000-word master&apos;s thesis in{" "}
              <span className="font-mono text-brand-purple-600 dark:text-brand-purple-400">15-25 minutes</span>, not{" "}
              <span className="line-through opacity-60">months</span>
            </p>
          </div>

          <p className="max-w-screen-sm mx-auto text-base text-muted-foreground leading-relaxed">
            AI-powered framework with 15 specialized agents. 100% open source (MIT), no coding skills required. Auto-citations from 200M+ research papers.
          </p>

          {/* GitHub Stats Badge */}
          <Link
            href="https://github.com/federicodeponte/opendraft"
            target="_blank"
            className="inline-block"
            aria-label="View OpenDraft on GitHub"
          >
            <Badge variant="outline" className="px-3 py-1.5 text-sm gap-2 hover:bg-accent/10 transition-colors cursor-pointer">
              <Github className="size-4" aria-hidden="true" />
              {githubLoading ? (
                <span>Loading...</span>
              ) : githubStats ? (
                <>
                  <Star className="size-4 fill-current" aria-hidden="true" />
                  <span>{formatNumber(githubStats.stars)} stars on GitHub</span>
                </>
              ) : (
                <span>View on GitHub</span>
              )}
            </Badge>
          </Link>

          <div className="flex flex-col sm:flex-row gap-4 items-center justify-center mt-8">
            <Button
              asChild
              size="lg"
              className="w-full sm:w-auto px-8 py-6 text-base font-semibold rounded-xl group shadow-lg hover:shadow-2xl hover:shadow-brand-purple-500/20 transition-all duration-cursor-slow bg-gradient-to-r from-brand-purple-500 to-brand-purple-600 hover:from-brand-purple-600 hover:to-brand-purple-700 text-white border-0"
            >
              <Link href="/waitlist" aria-label="Join waitlist for free thesis generation">
                Get Free Thesis (100/day)
                <ArrowRight className="size-5 ml-2 group-hover:translate-x-1 transition-transform duration-cursor" aria-hidden="true" />
              </Link>
            </Button>

            <Button
              asChild
              variant="outline"
              size="lg"
              className="w-full sm:w-auto px-8 py-6 text-base font-semibold rounded-xl border-2 border-brand-purple-200 dark:border-brand-purple-800 hover:border-brand-purple-400 dark:hover:border-brand-purple-600 hover:bg-brand-purple-50 dark:hover:bg-brand-purple-950 transition-all duration-cursor-slow"
            >
              <Link
                href="https://github.com/federicodeponte/opendraft#-quick-start-10-minutes"
                target="_blank"
                aria-label="View quick start guide on GitHub"
              >
                <Github className="size-5 mr-2" aria-hidden="true" />
                I&apos;m Technical, Skip to Code
              </Link>
            </Button>
          </div>

          <p className="text-xs text-muted-foreground max-w-md mx-auto">
            <AlertTriangle className="inline size-3 mr-1" />
            Check your institution&apos;s AI usage policy before using this tool. Learn more in <Link href="#faq" className="underline underline-offset-2 hover:text-accent transition-colors">FAQ</Link>.
          </p>
        </div>

        <div className="relative group mt-20 w-full">
          {/* Gradient background glow */}
          <div className="absolute inset-0 bg-gradient-to-r from-brand-purple-500/20 to-brand-cyan-500/20 blur-3xl -z-10" />

          {/* Hero visual - Real thesis screenshots carousel */}
          <Carousel
            className="w-full md:w-[900px] lg:w-[1000px] mx-auto"
            opts={{ loop: true, align: "center" }}
          >
            <CarouselContent className="-ml-4">
              {CAROUSEL_ITEMS.map((item, index) => (
                <CarouselItem key={index} className="pl-4">
                  <div className="relative aspect-[16/10] w-full bg-gradient-to-br from-white to-gray-50 dark:from-slate-900 dark:to-slate-800 p-8 rounded-2xl border-2 border-brand-purple-100 dark:border-brand-purple-900/50 shadow-2xl hover:shadow-brand-purple-500/20 transition-shadow duration-cursor-slow">
                    <Image
                      src={item.src}
                      alt={item.alt}
                      fill
                      className="object-contain rounded-xl"
                      priority={index === 0}
                      loading={index === 0 ? undefined : "lazy"}
                    />
                  </div>
                </CarouselItem>
              ))}
            </CarouselContent>
            <CarouselPrevious className="left-4 size-12 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm hover:bg-white dark:hover:bg-slate-900" aria-label="Previous slide" />
            <CarouselNext className="right-4 size-12 bg-white/80 dark:bg-slate-900/80 backdrop-blur-sm hover:bg-white dark:hover:bg-slate-900" aria-label="Next slide" />
          </Carousel>

          {/* Active slide indicators */}
          <div className="mt-6 flex justify-center gap-2">
            {CAROUSEL_ITEMS.map((_, index) => (
              <button
                key={index}
                className="h-2 w-2 rounded-full bg-brand-purple-300 dark:bg-brand-purple-700 hover:bg-brand-purple-500 dark:hover:bg-brand-purple-500 transition-all duration-cursor data-[active=true]:w-8 data-[active=true]:bg-brand-purple-500"
                aria-label={`Go to slide ${index + 1}`}
              />
            ))}
          </div>

          <div className="absolute bottom-0 left-0 w-full h-20 md:h-28 bg-gradient-to-b from-background/0 via-background/50 to-background rounded-lg pointer-events-none"></div>
        </div>
      </div>
    </section>
  );
};
