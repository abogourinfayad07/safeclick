import { Link } from "expo-router";
import { useState } from "react";
import { ScrollView, StyleSheet, Text, TextInput } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { ErrorText, PrimaryButton } from "@/components/ui";
import { COLORS } from "@/constants/theme";
import { api, errorMessage } from "@/lib/api";

export default function VerifyScreen() {
  const [token, setToken] = useState("");
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function verify() {
    setNotice("");
    setError("");
    setLoading(true);
    try {
      const response = await api.verify(token.trim());
      setNotice(response.message);
    } catch (cause) {
      setError(errorMessage(cause));
    } finally {
      setLoading(false);
    }
  }

  return (
    <SafeAreaView style={styles.safe} edges={["top"]}>
      <ScrollView contentContainerStyle={styles.content} keyboardShouldPersistTaps="handled">
        <Text style={styles.title}>Vérification de l'adresse</Text>
        <Text style={styles.subtitle}>
          En développement, le jeton est affiché dans les logs du serveur. Aucun e-mail payant
          n'est envoyé.
        </Text>

        <TextInput
          style={styles.input}
          value={token}
          onChangeText={setToken}
          placeholder="Jeton de vérification"
          placeholderTextColor={COLORS.muted}
          autoCapitalize="none"
          autoCorrect={false}
        />

        <PrimaryButton
          label={loading ? "Vérification…" : "Vérifier mon adresse"}
          onPress={() => void verify()}
          disabled={loading || token.trim().length < 20}
        />
        {notice ? <Text style={styles.notice}>{notice}</Text> : null}
        <ErrorText message={error} />
        <Link href="/login" style={styles.link}>Retour à la connexion</Link>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: COLORS.night },
  content: { padding: 20, paddingBottom: 40 },
  title: { color: COLORS.text, fontSize: 26, fontWeight: "800" },
  subtitle: { color: COLORS.muted, fontSize: 14, lineHeight: 20, marginTop: 8 },
  input: {
    backgroundColor: COLORS.surface,
    borderColor: "rgba(255,255,255,0.12)",
    borderWidth: 1,
    borderRadius: 12,
    color: COLORS.text,
    padding: 14,
    marginTop: 20,
    fontSize: 13,
  },
  notice: { color: "#86efac", fontSize: 13, lineHeight: 19, marginTop: 14 },
  link: { color: COLORS.electric, fontSize: 13, marginTop: 16 },
});
