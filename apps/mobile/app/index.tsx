import { Link } from "expo-router";
import { ScrollView, StyleSheet, Text, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { RISK_LABELS } from "@safeclick/shared";
import { COLORS } from "@/constants/theme";

export default function HomeScreen() {
  return (
    <SafeAreaView style={styles.safe} edges={["top"]}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.eyebrow}>CYBERSÉCURITÉ ACCESSIBLE</Text>
        <Text style={styles.title}>Repérez les arnaques avant de cliquer.</Text>
        <Text style={styles.subtitle}>
          SAFECLICK vous explique simplement ce qui est suspect dans un lien ou un message.
        </Text>

        <Link href={{ pathname: "/analyze", params: { kind: "url" } }} style={styles.card}>
          <Text style={styles.cardTitle}>Analyser un lien</Text>
          <Text style={styles.cardText}>
            Domaine, caractères inhabituels, sous-domaines et raccourcisseurs.
          </Text>
        </Link>

        <Link href={{ pathname: "/analyze", params: { kind: "message" } }} style={styles.card}>
          <Text style={styles.cardTitle}>Analyser un message</Text>
          <Text style={styles.cardText}>
            Urgence, demande d’argent, codes et usurpation d’identité.
          </Text>
        </Link>

        <View style={styles.levels}>
          <Text style={styles.levelsTitle}>Trois niveaux de risque</Text>
          <Text style={styles.level}>{RISK_LABELS.low}</Text>
          <Text style={styles.level}>{RISK_LABELS.medium}</Text>
          <Text style={styles.level}>{RISK_LABELS.high}</Text>
          <Text style={styles.disclaimer}>
            Un risque faible n’est jamais une garantie de sécurité.
          </Text>
        </View>

        <Text style={styles.note}>
          Navigation fonctionnelle. L’appel à l’API sera branché en phase 6, une fois le backend créé.
        </Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: COLORS.night },
  content: { padding: 20, paddingBottom: 40 },
  eyebrow: { color: COLORS.electric, fontSize: 12, fontWeight: "700", letterSpacing: 2 },
  title: { color: COLORS.text, fontSize: 30, fontWeight: "800", marginTop: 12 },
  subtitle: { color: COLORS.muted, fontSize: 15, lineHeight: 22, marginTop: 12 },
  card: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.1)",
    padding: 18,
    marginTop: 16,
  },
  cardTitle: { color: COLORS.text, fontSize: 17, fontWeight: "700" },
  cardText: { color: COLORS.muted, fontSize: 13, lineHeight: 19, marginTop: 6 },
  levels: { marginTop: 28 },
  levelsTitle: { color: COLORS.text, fontSize: 17, fontWeight: "700", marginBottom: 10 },
  level: { color: COLORS.text, fontSize: 14, paddingVertical: 3 },
  disclaimer: { color: COLORS.muted, fontSize: 12, marginTop: 10 },
  note: { color: COLORS.muted, fontSize: 12, lineHeight: 18, marginTop: 28 },
});
