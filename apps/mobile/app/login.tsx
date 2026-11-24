import { Link, router } from "expo-router";
import { useState } from "react";
import { ScrollView, StyleSheet, Text, TextInput } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { ErrorText, PrimaryButton } from "@/components/ui";
import { COLORS } from "@/constants/theme";
import { api, errorMessage } from "@/lib/api";
import { setToken } from "@/lib/token";

export default function LoginScreen() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function login() {
    setError("");
    setLoading(true);
    try {
      const response = await api.login(email.trim(), password);
      await setToken(response.access_token);
      router.replace("/profile");
    } catch (cause) {
      setError(errorMessage(cause));
    } finally {
      setLoading(false);
    }
  }

  return (
    <SafeAreaView style={styles.safe} edges={["top"]}>
      <ScrollView contentContainerStyle={styles.content} keyboardShouldPersistTaps="handled">
        <Text style={styles.title}>Connexion</Text>
        <Text style={styles.subtitle}>
          Votre adresse doit avoir été vérifiée avant la connexion.
        </Text>

        <TextInput
          style={styles.input}
          value={email}
          onChangeText={setEmail}
          placeholder="Adresse e-mail"
          placeholderTextColor={COLORS.muted}
          autoCapitalize="none"
          keyboardType="email-address"
          autoCorrect={false}
        />
        <TextInput
          style={styles.input}
          value={password}
          onChangeText={setPassword}
          placeholder="Mot de passe"
          placeholderTextColor={COLORS.muted}
          secureTextEntry
        />

        <PrimaryButton
          label={loading ? "Connexion…" : "Se connecter"}
          onPress={() => void login()}
          disabled={loading || !email || !password}
        />
        <ErrorText message={error} />

        <Link href="/register" style={styles.link}>
          Pas encore de compte ? Inscription
        </Link>
        <Link href="/verify" style={styles.link}>
          Vérifier mon adresse
        </Link>
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
    marginTop: 14,
    fontSize: 14,
  },
  link: { color: COLORS.electric, fontSize: 13, marginTop: 16 },
});
