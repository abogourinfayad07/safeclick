import { Link } from "expo-router";
import { useState } from "react";
import { ScrollView, StyleSheet, Text, TextInput } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { ErrorText, PrimaryButton } from "@/components/ui";
import { COLORS } from "@/constants/theme";
import { api, errorMessage } from "@/lib/api";

export default function RegisterScreen() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function register() {
    setNotice("");
    setError("");
    setLoading(true);
    try {
      const response = await api.register(email.trim(), password);
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
        <Text style={styles.title}>Créer un compte</Text>
        <Text style={styles.subtitle}>
          12 caractères minimum, avec une lettre et un chiffre. Aucun service payant.
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
          label={loading ? "Création…" : "Créer le compte"}
          onPress={() => void register()}
          disabled={loading || !email || password.length < 12}
        />
        {notice ? <Text style={styles.notice}>{notice}</Text> : null}
        <ErrorText message={error} />

        <Link href="/login" style={styles.link}>Déjà un compte ? Connexion</Link>
        <Link href="/verify" style={styles.link}>J'ai un jeton de vérification</Link>
        <Link href="/profile" style={styles.link}>Voir mon profil</Link>
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
  notice: { color: "#86efac", fontSize: 13, lineHeight: 19, marginTop: 14 },
  link: { color: COLORS.electric, fontSize: 13, marginTop: 16 },
});
