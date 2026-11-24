import { useLocalSearchParams } from "expo-router";
import { useState } from "react";
import { ScrollView, StyleSheet, Text, TextInput, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { ANALYSIS_LIMITS, type AnalysisResult } from "@safeclick/shared";
import { AnalysisResultCard } from "@/components/analysis-result";
import { ErrorText, PrimaryButton } from "@/components/ui";
import { COLORS } from "@/constants/theme";
import { api, errorMessage } from "@/lib/api";

export default function AnalyzeScreen() {
  const { kind } = useLocalSearchParams<{ kind?: string }>();
  const isUrl = kind !== "message";
  const [value, setValue] = useState("");
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const limit = isUrl ? ANALYSIS_LIMITS.urlMaxLength : ANALYSIS_LIMITS.messageMaxLength;

  async function analyze() {
    setError("");
    setResult(null);
    setLoading(true);
    try {
      const data = isUrl ? await api.analyzeUrl(value) : await api.analyzeMessage(value);
      setResult(data);
    } catch (cause) {
      setError(errorMessage(cause));
    } finally {
      setLoading(false);
    }
  }

  return (
    <SafeAreaView style={styles.safe} edges={["top"]}>
      <ScrollView contentContainerStyle={styles.content} keyboardShouldPersistTaps="handled">
        <Text style={styles.title}>
          {isUrl ? "Analyser un lien" : "Analyser un message"}
        </Text>
        <Text style={styles.subtitle}>
          {isUrl
            ? "Collez l'URL à vérifier. Le serveur ne l'ouvrira pas."
            : "Collez le SMS ou le message WhatsApp suspect."}
        </Text>

        <TextInput
          style={styles.input}
          value={value}
          onChangeText={setValue}
          maxLength={limit}
          multiline={!isUrl}
          placeholder={isUrl ? "https://exemple.com/..." : "Message reçu..."}
          placeholderTextColor={COLORS.muted}
          autoCapitalize="none"
          autoCorrect={false}
        />

        <PrimaryButton
          label={loading ? "Analyse en cours…" : "Analyser"}
          onPress={() => void analyze()}
          disabled={loading || value.trim().length < 3}
        />
        <ErrorText message={error} />

        {result ? <AnalysisResultCard result={result} /> : null}

        <Text style={styles.note}>
          Longueur maximale : {limit} caractères. Analyse passive : aucun lien n'est visité
          par le serveur.
        </Text>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: COLORS.night },
  content: { padding: 20, paddingBottom: 40 },
  title: { color: COLORS.text, fontSize: 24, fontWeight: "800" },
  subtitle: { color: COLORS.muted, fontSize: 14, lineHeight: 20, marginTop: 8 },
  input: {
    backgroundColor: COLORS.surface,
    borderColor: "rgba(255,255,255,0.12)",
    borderWidth: 1,
    borderRadius: 12,
    color: COLORS.text,
    minHeight: 100,
    padding: 14,
    marginTop: 20,
    fontSize: 14,
  },
  note: { color: COLORS.muted, fontSize: 12, lineHeight: 18, marginTop: 24 },
});
