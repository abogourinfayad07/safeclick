import { Link } from "expo-router";
import { useEffect, useState } from "react";
import { ScrollView, StyleSheet, Text } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { RISK_LABELS } from "@safeclick/shared";
import { Card, ErrorText } from "@/components/ui";
import { COLORS } from "@/constants/theme";
import { api, errorMessage, type HistoryItem } from "@/lib/api";
import { getToken } from "@/lib/token";

export default function HistoryScreen() {
  const [items, setItems] = useState<HistoryItem[]>([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [authenticated, setAuthenticated] = useState(true);

  useEffect(() => {
    let active = true;
    void (async () => {
      if (!(await getToken())) {
        if (active) {
          setAuthenticated(false);
          setLoading(false);
        }
        return;
      }
      try {
        const page = await api.listAnalyses(50, 0);
        if (active) setItems(page.items);
      } catch (cause) {
        if (active) setError(errorMessage(cause));
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => {
      active = false;
    };
  }, []);

  return (
    <SafeAreaView style={styles.safe} edges={["top"]}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.title}>Historique des analyses</Text>
        {!authenticated ? (
          <Link href="/login" style={styles.link}>Connectez-vous pour voir votre historique</Link>
        ) : loading ? (
          <Text style={styles.muted}>Chargement…</Text>
        ) : (
          <>
            <ErrorText message={error} />
            {items.length === 0 ? (
              <Text style={styles.muted}>Vous n'avez encore analysé aucun contenu.</Text>
            ) : (
              items.map((item) => (
                <Card key={item.id}>
                  <Text style={styles.row}>
                    {item.kind.toUpperCase()} — {RISK_LABELS[item.riskLevel]} — {item.score}/100
                  </Text>
                  <Text style={styles.preview}>{item.inputPreview ?? "—"}</Text>
                  <Text style={styles.date}>{new Date(item.createdAt).toLocaleString()}</Text>
                </Card>
              ))
            )}
          </>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: COLORS.night },
  content: { padding: 20, paddingBottom: 40 },
  title: { color: COLORS.text, fontSize: 26, fontWeight: "800" },
  muted: { color: COLORS.muted, fontSize: 13, lineHeight: 19, marginTop: 16 },
  link: { color: COLORS.electric, fontSize: 14, marginTop: 16 },
  row: { color: COLORS.text, fontSize: 13, fontWeight: "700" },
  preview: { color: COLORS.muted, fontSize: 12, marginTop: 6 },
  date: { color: COLORS.muted, fontSize: 11, marginTop: 6 },
});
