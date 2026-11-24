import Link from "next/link";
import { ArrowRight, Link2, MessageSquare, ShieldCheck } from "lucide-react";
import { buttonVariants } from "@/components/ui/button";
import { RiskBadge } from "@/components/analysis/risk-badge";

const features = [
  {
    icon: Link2,
    title: "Analyse de liens",
    description:
      "Structure de l’URL, domaine, caractères inhabituels, sous-domaines trompeurs et raccourcisseurs.",
  },
  {
    icon: MessageSquare,
    title: "Analyse de messages",
    description:
      "Urgence, demande d’argent, codes de vérification, promesses de gains et usurpation d’identité.",
  },
  {
    icon: ShieldCheck,
    title: "Signalement modéré",
    description:
      "Un contact suspect peut être signalé, mais jamais accusé automatiquement : la modération décide.",
  },
];

export default function HomePage() {
  return (
    <>
      <section className="relative overflow-hidden border-b border-white/10">
        <div className="absolute inset-0 -z-10 bg-[radial-gradient(circle_at_50%_0%,rgba(37,99,235,0.18),transparent_60%)]" />
        <div className="mx-auto max-w-6xl px-4 py-20 sm:px-6 sm:py-28">
          <p className="mb-4 text-sm font-semibold uppercase tracking-[0.2em] text-electric-300">
            Cybersécurité accessible
          </p>
          <h1 className="max-w-3xl text-4xl font-bold leading-tight tracking-tight sm:text-6xl">
            Repérez les arnaques avant de cliquer.
          </h1>
          <p className="mt-6 max-w-2xl text-lg leading-relaxed text-slate-300">
            SAFECLICK analyse les liens et les messages suspects, puis vous explique
            simplement ce qui est dangereux et quoi faire — même sans connaissance technique.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link href="#fonctionnalites" className={buttonVariants({ size: "lg" })}>
              Découvrir SAFECLICK <ArrowRight className="h-4 w-4" aria-hidden="true" />
            </Link>
            <Link
              href="#confidentialite"
              className={buttonVariants({ variant: "outline", size: "lg" })}
            >
              Notre approche confidentialité
            </Link>
          </div>
          <p className="mt-5 text-xs text-slate-500">
            Interface en cours de construction : l’analyse sera connectée à l’API lors de la phase 5.
          </p>
        </div>
      </section>

      <section id="mission" className="mx-auto max-w-6xl px-4 py-16 sm:px-6">
        <h2 className="text-2xl font-bold sm:text-3xl">Notre mission</h2>
        <p className="mt-4 max-w-3xl leading-relaxed text-slate-300">
          En Afrique francophone, beaucoup d’internautes reçoivent de faux liens de connexion,
          de fausses offres d’emploi ou des demandes d’argent urgentes. SAFECLICK rend la
          prévention compréhensible, gratuite et utilisable sur téléphone comme sur ordinateur.
        </p>
      </section>

      <section id="fonctionnalites" className="border-y border-white/10 bg-night-900/40">
        <div className="mx-auto max-w-6xl px-4 py-16 sm:px-6">
          <h2 className="text-2xl font-bold sm:text-3xl">Trois réflexes de protection</h2>
          <div className="mt-8 grid gap-5 md:grid-cols-3">
            {features.map((feature) => (
              <article
                key={feature.title}
                className="rounded-2xl border border-white/10 bg-night-800/50 p-6"
              >
                <feature.icon className="h-7 w-7 text-electric-400" aria-hidden="true" />
                <h3 className="mt-4 text-lg font-semibold">{feature.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-slate-300">
                  {feature.description}
                </p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section id="niveaux" className="mx-auto max-w-6xl px-4 py-16 sm:px-6">
        <h2 className="text-2xl font-bold sm:text-3xl">Trois niveaux, zéro jargon</h2>
        <div className="mt-8 flex flex-wrap items-center gap-4">
          <RiskBadge level="low" />
          <RiskBadge level="medium" />
          <RiskBadge level="high" />
        </div>
        <p className="mt-5 max-w-3xl text-sm leading-relaxed text-slate-300">
          Chaque résultat affiche un score indicatif, les éléments détectés, des
          recommandations et les limites de l’analyse. Un risque faible{" "}
          <strong className="text-white">n’est jamais une garantie de sécurité</strong>.
        </p>
      </section>

      <section id="confidentialite" className="border-t border-white/10 bg-night-900/40">
        <div className="mx-auto max-w-6xl px-4 py-16 sm:px-6">
          <h2 className="text-2xl font-bold sm:text-3xl">Vos données restent à vous</h2>
          <p className="mt-4 max-w-3xl leading-relaxed text-slate-300">
            Les secrets ne sont jamais stockés dans le code, les mots de passe sont hachés avec
            Argon2id, et les signalements restent non vérifiés jusqu’à modération. Aucune URL
            soumise n’est ouverte depuis le serveur pendant la phase de développement.
          </p>
        </div>
      </section>
    </>
  );
}
