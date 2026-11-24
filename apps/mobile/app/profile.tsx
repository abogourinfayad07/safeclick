import { Link, router } from "expo-router";
import { useEffect, useState } from "react";
import { ScrollView, StyleSheet, Text } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { Card, ErrorText, PrimaryButton } from "@/components/ui";
import { COLORS } from "@/constants/theme";
import { api, errorMessage, type UserProfile } from "@/lib/api";
import { clearToken, getToken } from "@/lib/token";

export default function ProfileScreen() {
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [authenticated, setAuthenticated] = useState(true);
  const [confirming, setConfirming] = useState(false);

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
        const data = await api.getProfile();
        if (active) setProfile(data);
      } catch (cause) {
        if (active) {
          setError(errorMessage(cause));
          await clearToken();
          setAuthenticated(false);
        }
      } finally {
        if (active) setLoading(false);
      }
    })();
    return () => {
      active = false;
    };
  }, []);

  async function logout() {
    await clearToken();
    router.replace("/");
  }

  async function removeAccount() {
    setError("");
    try {
      await api.deleteProfile();
    } catch (cause) {
      setError(errorMessage(cause));
      return;
    }
    await clearToken();
    router.replace("/");
  }

  return (
    <SafeAreaView style={styles.safe} edges={["top"]}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.title}>Mon profil</Text>
        {!authenticated ? (
          <Link href="/login" style={styles.link}>Connectez-vous pour voir votre profil</Link>
        ) : loading ? (
          <Text style={styles.muted}>Chargement…</Text>
        ) : (
          <>
            <ErrorText message={error} />
            {profile ? (
              <Card>
                <Text style={styles.row}>{profile.email}</Text>
                <Text style={styles.muted}>Rôle : {profile.role}</Text>
                <Text style={styles.muted}>
                  Adresse vérifiée : {profile.isVerified ? "oui" : "non"}
                </Text>
                <Text style={styles.muted}>
                  Créé le : {new Date(profile.createdAt).toLocaleString()}
                </Text>
              </Card>
            ) : null}

            <Link href="/history" style={styles.link}>Voir mon historique</Link>
            <Link href="/settings" style={styles.link}>Paramètres et confidentialité</Link>

            <PrimaryButton label="Se déconnecter" onPress={() => void logout()} />

            <Card>
              <Text style={styles.dangerTitle}>Supprimer mon compte</Text>
              <Text style={styles.muted}>
                Cette action supprime le compte et rend les jetons existants invalides.
              </Text>
              {confirming ? (
                <PrimaryButton
                  label="Confirmer la suppression définitive"
                  onPress={() => void removeAccount()}
                />
              ) : (
                <PrimaryButton label="Supprimer mon compte" onPress={() => setConfirming(true)} />
              )}
            </Card>
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
  muted: { color: COLORS.muted, fontSize: 12, lineHeight: 18, marginTop: 8 },
  link: { color: COLORS.electric, fontSize: 14, marginTop: 16 },
  row: { color: COLORS.text, fontSize: 15, fontWeight: "700" },
  dangerTitle: { color: "#fca5a5", fontSize: 15, fontWeight: "700" },
});
