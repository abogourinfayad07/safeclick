import { useLocalSearchParams } from "expo-router";
import { useState } from "react";
import { ScrollView, StyleSheet, Text, TextInput, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { ANALYSIS_LIMITS } from "@safeclick/shared";
import { COLORS } from "@/constants/theme";

export default function AnalyzeScreen() {
  const { kind } = useLocalSearchParams<{ kind?: string }>();
  const isUrl = kind !== "message";
  const [value, setValue] = useState("");
  const limit = isUrl ? ANALYSIS_LIMITS.urlMaxLength : ANALYSIS_LIMITS.messageMaxLength;

  return (
    <SafeAreaView style={styles.safe} edges={["top"]}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.title}>
          {isUrl ? "Analyser un lien" : "Analyser un message"}
        </Text>
        <Text style={styles.subtitle}>
          {isUrl
            ? "Collez l’URL à vérifier. Le serveur ne l’ouvrira pas."
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

        <View style={styles.disabledButton}>
          <Text style={styles.disabledText}>Analyse — connexion API en phase 6</Text>
        </View>

        <Text style={styles.note}>
          Longueur maximale : {limit} caractères. Aucune analyse n’est effectuée tant que
          l’API n’est pas connectée : aucun résultat fictif n’est affiché.
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
  disabledButton: {
    backgroundColor: "rgba(255,255,255,0.06)",
    borderRadius: 12,
    padding: 14,
    marginTop: 14,
    alignItems: "center",
  },
  disabledText: { color: COLORS.muted, fontSize: 14, fontWeight: "600" },
  note: { color: COLORS.muted, fontSize: 12, lineHeight: 18, marginTop: 24 },
});
