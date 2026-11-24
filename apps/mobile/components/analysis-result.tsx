import { StyleSheet, Text, View } from "react-native";
import { RISK_LABELS, type AnalysisResult } from "@safeclick/shared";
import { COLORS } from "@/constants/theme";
import { Card, Disclaimer } from "./ui";

const COLORS_BY_LEVEL = {
  low: COLORS.low,
  medium: COLORS.medium,
  high: COLORS.high,
} as const;

export function AnalysisResultCard({ result }: { result: AnalysisResult }) {
  return (
    <Card>
      <Text style={styles.heading}>Résultat de l'analyse</Text>
      <View style={styles.badgeRow}>
        <View style={[styles.badge, { backgroundColor: COLORS_BY_LEVEL[result.riskLevel] }]}>
          <Text style={styles.badgeText}>{RISK_LABELS[result.riskLevel]}</Text>
        </View>
        <Text style={styles.score}>{result.score}/100</Text>
      </View>

      <Text style={styles.section}>Éléments détectés</Text>
      {result.indicators.length === 0 ? (
        <Text style={styles.muted}>Aucun signal détecté par les règles actuelles.</Text>
      ) : (
        result.indicators.map((indicator) => (
          <View key={indicator.code} style={styles.indicator}>
            <Text style={styles.indicatorTitle}>
              {indicator.label} (+{indicator.weight})
            </Text>
            <Text style={styles.muted}>{indicator.detail}</Text>
          </View>
        ))
      )}

      <Text style={styles.section}>Que faire</Text>
      {result.recommendations.map((item) => (
        <Text key={item} style={styles.listItem}>• {item}</Text>
      ))}

      <Text style={styles.section}>Limites de l'analyse</Text>
      {result.limitations.map((item) => (
        <Text key={item} style={styles.muted}>• {item}</Text>
      ))}

      <Disclaimer>
        Résultat indicatif. Un risque faible n'est jamais une garantie de sécurité.
      </Disclaimer>
    </Card>
  );
}

const styles = StyleSheet.create({
  heading: { color: COLORS.text, fontSize: 18, fontWeight: "800" },
  badgeRow: { flexDirection: "row", alignItems: "center", justifyContent: "space-between", marginTop: 12 },
  badge: { borderRadius: 999, paddingHorizontal: 12, paddingVertical: 5 },
  badgeText: { color: "#ffffff", fontSize: 12, fontWeight: "700" },
  score: { color: COLORS.text, fontSize: 20, fontWeight: "800" },
  section: { color: COLORS.text, fontSize: 14, fontWeight: "700", marginTop: 18 },
  muted: { color: COLORS.muted, fontSize: 12, lineHeight: 18, marginTop: 5 },
  indicator: { marginTop: 10 },
  indicatorTitle: { color: COLORS.text, fontSize: 13, fontWeight: "700" },
  listItem: { color: COLORS.text, fontSize: 12, lineHeight: 18, marginTop: 4 },
});
