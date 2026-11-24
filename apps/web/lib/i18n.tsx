"use client";

import { createContext, useContext, type ReactNode } from "react";

export const locales = ["fr", "en"] as const;
export type Locale = (typeof locales)[number];

const fr = {
  nav_mission: "Mission",
  nav_features: "Fonctionnalités",
  nav_levels: "Niveaux de risque",
  nav_privacy: "Confidentialité",
  nav_analyze: "Analyser",
  nav_report: "Signaler",
  nav_login: "Connexion",
  nav_register: "Inscription",
  nav_dashboard: "Tableau de bord",
  nav_admin: "Administration",
  nav_logout: "Déconnexion",

  common_loading: "Analyse en cours…",
  common_error: "Une erreur est survenue. Réessayez.",
  common_retry: "Réessayer",
  common_submit: "Envoyer",
  common_cancel: "Annuler",
  common_disclaimer: "Résultat indicatif. Un risque faible n'est jamais une garantie de sécurité.",
  common_required: "Ce champ est obligatoire.",

  home_eyebrow: "Cybersécurité accessible",
  home_title: "Repérez les arnaques avant de cliquer.",
  home_subtitle:
    "SAFECLICK analyse les liens et les messages suspects, puis vous explique simplement ce qui est dangereux et quoi faire — même sans connaissance technique.",
  home_cta: "Analyser un lien",
  home_privacy_cta: "Notre approche confidentialité",
  home_mission_title: "Notre mission",
  home_mission_text:
    "En Afrique francophone, beaucoup d'internautes reçoivent de faux liens de connexion, de fausses offres d'emploi ou des demandes d'argent urgentes. SAFECLICK rend la prévention compréhensible, gratuite et utilisable sur téléphone comme sur ordinateur.",
  home_features_title: "Trois réflexes de protection",
  feature_link_title: "Analyse de liens",
  feature_link_text:
    "Structure de l'URL, domaine, caractères inhabituels, sous-domaines trompeurs et raccourcisseurs.",
  feature_message_title: "Analyse de messages",
  feature_message_text:
    "Urgence, demande d'argent, codes de vérification, promesses de gains et usurpation d'identité.",
  feature_report_title: "Signalement modéré",
  feature_report_text:
    "Un contact suspect peut être signalé, mais jamais accusé automatiquement : la modération décide.",
  home_levels_title: "Trois niveaux, zéro jargon",
  home_levels_text:
    "Chaque résultat affiche un score indicatif, les éléments détectés, des recommandations et les limites de l'analyse.",
  home_privacy_title: "Vos données restent à vous",
  home_privacy_text:
    "Les secrets ne sont jamais stockés dans le code, les mots de passe sont hachés avec Argon2id, et les signalements restent non vérifiés jusqu'à modération. Aucune URL soumise n'est ouverte depuis le serveur.",

  analyze_title: "Analyser un contenu suspect",
  analyze_subtitle: "Collez un lien ou un message. SAFECLICK n'ouvre pas le lien : il analyse seulement la chaîne fournie.",
  analyze_tab_url: "Lien",
  analyze_tab_message: "Message",
  analyze_url_label: "Adresse du lien",
  analyze_url_placeholder: "https://exemple.fr/page",
  analyze_message_label: "Texte du message",
  analyze_message_placeholder: "Collez ici le message reçu…",
  analyze_submit: "Analyser",
  analyze_result_title: "Résultat de l'analyse",
  analyze_score: "Score indicatif",
  analyze_indicators: "Éléments détectés",
  analyze_recommendations: "Que faire",
  analyze_limitations: "Limites de l'analyse",
  analyze_no_indicators: "Aucun signal détecté par les règles actuelles.",

  report_title: "Signaler un contact suspect",
  report_subtitle: "Le contact est haché avant stockage. Aucune accusation n'est faite automatiquement.",
  report_kind_label: "Type de contact",
  report_contact_label: "Contact",
  report_reason_label: "Motif",
  report_ack: "Je comprends qu'un signalement n'est pas une preuve.",
  report_submit: "Envoyer le signalement",
  report_success: "Signalement enregistré pour vérification.",
  report_duplicate: "Ce signalement avait déjà été enregistré.",

  auth_login_title: "Connexion",
  auth_register_title: "Créer un compte",
  auth_email: "Adresse e-mail",
  auth_password: "Mot de passe",
  auth_password_hint: "12 caractères minimum, avec une lettre et un chiffre.",
  auth_login_submit: "Se connecter",
  auth_register_submit: "Créer le compte",
  auth_no_account: "Pas encore de compte ?",
  auth_has_account: "Déjà un compte ?",
  auth_token: "Jeton de vérification",
  auth_verify_title: "Vérification de l'adresse",
  auth_verify_text: "En développement, le jeton de vérification est affiché dans les logs du serveur.",
  auth_verify_submit: "Vérifier mon adresse",
  auth_verify_success: "Adresse vérifiée. Vous pouvez vous connecter.",

  dashboard_title: "Tableau de bord",
  dashboard_subtitle: "Vos analyses réelles et les statistiques mesurées sur la base locale.",
  dashboard_history: "Analyses récentes",
  dashboard_empty: "Aucune analyse enregistrée pour ce compte.",
  dashboard_view_all: "Voir tout l'historique",
  dashboard_stats_users: "Comptes",
  dashboard_stats_reports: "Signalements",
  dashboard_stats_analyses: "Analyses",

  history_title: "Historique des analyses",
  history_empty: "Vous n'avez encore analysé aucun contenu.",
  history_date: "Date",
  history_kind: "Type",
  history_score: "Score",
  history_level: "Niveau",
  history_preview: "Extrait",

  profile_title: "Mon profil",
  profile_email: "E-mail",
  profile_role: "Rôle",
  profile_verified: "Adresse vérifiée",
  profile_created: "Créé le",
  profile_delete: "Supprimer mon compte",
  profile_delete_confirm: "Confirmer la suppression définitive",
  profile_delete_warning: "Cette action supprime le compte et rend les jetons existants invalides.",

  admin_title: "Administration",
  admin_reports: "Signalements à modérer",
  admin_stats: "Statistiques mesurées",
  admin_review_confirm: "Confirmer",
  admin_review_dismiss: "Écarter",
  admin_reviewed: "Signalement modéré.",
  admin_empty: "Aucun signalement à afficher.",

  about_title: "À propos de SAFECLICK",
  about_text:
    "SAFECLICK est un projet de cybersécurité développé au Bénin pour rendre la prévention compréhensible en Afrique francophone. Le moteur repose d'abord sur des règles explicites, vérifiables et sans appel réseau.",
  privacy_title: "Confidentialité",
  privacy_text:
    "Les contacts signalés sont hachés avec HMAC-SHA256. Les analyses conservent un extrait limité et un hachage, jamais le contenu complet. Les mots de passe utilisent Argon2id. En développement, la vérification d'e-mail se fait dans les logs serveur.",
  legal_title: "Mentions légales",
  legal_text:
    "SAFECLICK est un projet en cours de développement. Aucune offre commerciale ni paiement n'est actif. Les résultats fournis sont indicatifs et ne constituent pas un avis juridique ou une preuve d'arnaque.",
  help_title: "Aide et questions fréquentes",
  help_text:
    "Un risque faible ne garantit pas la sécurité d'un lien. Vérifiez toujours l'expéditeur par un autre canal, ne transmettez jamais de code reçu par SMS et tapez l'adresse connue du site dans votre navigateur.",
  security_title: "Sécurité de l'analyse",
  security_text:
    "L'analyse est passive : le serveur ne visite aucun lien soumis. Les règles utilisées sont publiques dans le code et leurs limites sont affichées avec chaque résultat.",
  contact_title: "Contact",
  contact_text:
    "Aucun service d'e-mail payant n'est utilisé. En développement, les messages de vérification sont écrits dans les logs du serveur. Les canaux publics seront documentés lors du déploiement.",

  footer_rights: "© 2026 SAFECLICK — Développé au Bénin pour l'Afrique francophone.",
} as const;

type Dictionary = { [Key in keyof typeof fr]: string };

const en: Dictionary = {
  nav_mission: "Mission",
  nav_features: "Features",
  nav_levels: "Risk levels",
  nav_privacy: "Privacy",
  nav_analyze: "Analyze",
  nav_report: "Report",
  nav_login: "Log in",
  nav_register: "Sign up",
  nav_dashboard: "Dashboard",
  nav_admin: "Admin",
  nav_logout: "Log out",
  common_loading: "Analyzing…",
  common_error: "Something went wrong. Please try again.",
  common_retry: "Try again",
  common_submit: "Submit",
  common_cancel: "Cancel",
  common_disclaimer: "Indicative result. Low risk is never a security guarantee.",
  common_required: "This field is required.",
  home_eyebrow: "Accessible cybersecurity",
  home_title: "Spot scams before you click.",
  home_subtitle:
    "SAFECLICK analyzes suspicious links and messages, then explains clearly what is risky and what to do — no technical knowledge needed.",
  home_cta: "Analyze a link",
  home_privacy_cta: "Our privacy approach",
  home_mission_title: "Our mission",
  home_mission_text:
    "In French-speaking Africa, many internet users receive fake login links, fake job offers or urgent money requests. SAFECLICK makes prevention understandable, free and usable on both phone and computer.",
  home_features_title: "Three protective reflexes",
  feature_link_title: "Link analysis",
  feature_link_text: "URL structure, domain, unusual characters, misleading subdomains and shorteners.",
  feature_message_title: "Message analysis",
  feature_message_text: "Urgency, money requests, verification codes, prize promises and impersonation.",
  feature_report_title: "Moderated reporting",
  feature_report_text: "A contact can be reported, never automatically accused: moderators decide.",
  home_levels_title: "Three levels, no jargon",
  home_levels_text:
    "Each result shows an indicative score, detected signals, recommendations and analysis limits.",
  home_privacy_title: "Your data stays yours",
  home_privacy_text:
    "Secrets are never stored in code, passwords are hashed with Argon2id, and reports stay unverified until moderation. Submitted URLs are never opened by the server.",
  analyze_title: "Analyze suspicious content",
  analyze_subtitle: "Paste a link or a message. SAFECLICK never visits the link: only the provided string is analyzed.",
  analyze_tab_url: "Link",
  analyze_tab_message: "Message",
  analyze_url_label: "Link address",
  analyze_url_placeholder: "https://example.com/page",
  analyze_message_label: "Message text",
  analyze_message_placeholder: "Paste the received message here…",
  analyze_submit: "Analyze",
  analyze_result_title: "Analysis result",
  analyze_score: "Indicative score",
  analyze_indicators: "Detected signals",
  analyze_recommendations: "What to do",
  analyze_limitations: "Analysis limits",
  analyze_no_indicators: "No signal detected by the current rules.",
  report_title: "Report a suspicious contact",
  report_subtitle: "The contact is hashed before storage. No accusation is made automatically.",
  report_kind_label: "Contact type",
  report_contact_label: "Contact",
  report_reason_label: "Reason",
  report_ack: "I understand that a report is not proof.",
  report_submit: "Submit report",
  report_success: "Report saved for verification.",
  report_duplicate: "This report had already been recorded.",
  auth_login_title: "Log in",
  auth_register_title: "Create an account",
  auth_email: "Email address",
  auth_password: "Password",
  auth_password_hint: "At least 12 characters, with a letter and a number.",
  auth_login_submit: "Log in",
  auth_register_submit: "Create account",
  auth_no_account: "No account yet?",
  auth_has_account: "Already have an account?",
  auth_token: "Verification token",
  auth_verify_title: "Address verification",
  auth_verify_text: "In development, the verification token is printed in the server logs.",
  auth_verify_submit: "Verify my address",
  auth_verify_success: "Address verified. You can now log in.",
  dashboard_title: "Dashboard",
  dashboard_subtitle: "Your real analyses and statistics measured on the local database.",
  dashboard_history: "Recent analyses",
  dashboard_empty: "No analysis recorded for this account.",
  dashboard_view_all: "View full history",
  dashboard_stats_users: "Accounts",
  dashboard_stats_reports: "Reports",
  dashboard_stats_analyses: "Analyses",
  history_title: "Analysis history",
  history_empty: "You have not analyzed any content yet.",
  history_date: "Date",
  history_kind: "Type",
  history_score: "Score",
  history_level: "Level",
  history_preview: "Preview",
  profile_title: "My profile",
  profile_email: "Email",
  profile_role: "Role",
  profile_verified: "Address verified",
  profile_created: "Created on",
  profile_delete: "Delete my account",
  profile_delete_confirm: "Confirm permanent deletion",
  profile_delete_warning: "This deletes the account and invalidates existing tokens.",
  admin_title: "Administration",
  admin_reports: "Reports to moderate",
  admin_stats: "Measured statistics",
  admin_review_confirm: "Confirm",
  admin_review_dismiss: "Dismiss",
  admin_reviewed: "Report moderated.",
  admin_empty: "No report to display.",
  about_title: "About SAFECLICK",
  about_text:
    "SAFECLICK is a cybersecurity project developed in Benin to make prevention understandable in French-speaking Africa. The engine first relies on explicit, verifiable rules with no network calls.",
  privacy_title: "Privacy",
  privacy_text:
    "Reported contacts are hashed with HMAC-SHA256. Analyses keep a limited preview and a hash, never the full content. Passwords use Argon2id. In development, email verification happens in server logs.",
  legal_title: "Legal notice",
  legal_text:
    "SAFECLICK is a work in progress. No commercial offer or payment is active. Results are indicative and are neither legal advice nor proof of a scam.",
  help_title: "Help and frequently asked questions",
  help_text:
    "Low risk does not guarantee a link is safe. Always verify the sender through another channel, never share a code received by SMS, and type the known site address in your browser.",
  security_title: "Analysis security",
  security_text:
    "Analysis is passive: the server never visits submitted links. The rules are public in the code and their limits are shown with every result.",
  contact_title: "Contact",
  contact_text:
    "No paid email service is used. In development, verification messages are written to server logs. Public channels will be documented at deployment time.",
  footer_rights: "© 2026 SAFECLICK — Developed in Benin for French-speaking Africa.",
};

export const dictionaries: Record<Locale, Dictionary> = { fr, en };

export function getDictionary(locale: Locale): Dictionary {
  return dictionaries[locale] ?? fr;
}

export type TranslationKey = keyof Dictionary;

interface I18nValue {
  locale: Locale;
  t: (key: TranslationKey) => string;
}

const I18nContext = createContext<I18nValue>({
  locale: "fr",
  t: (key) => getDictionary("fr")[key],
});

export function I18nProvider({
  locale = "fr",
  children,
}: {
  locale?: Locale;
  children: ReactNode;
}) {
  const dictionary = getDictionary(locale);
  return (
    <I18nContext.Provider value={{ locale, t: (key) => dictionary[key] }}>
      {children}
    </I18nContext.Provider>
  );
}

export function useT(): (key: TranslationKey) => string {
  return useContext(I18nContext).t;
}

export function useLocale(): Locale {
  return useContext(I18nContext).locale;
}
