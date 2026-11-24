import { Link } from "expo-router";
import { ScrollView, StyleSheet, Text } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { Card, Disclaimer } from "@/components/ui";
import { COLORS } from "@/constants/theme";
import { API_URL } from "@/lib/api";
import { clearToken } from "@/lib/token";

export default function SettingsScreen() {
  return (
    <SafeAreaView style={styles.safe} edges={["top"]}>
      <ScrollView contentContainerStyle={styles.content}>
        <Text style={styles.title}>Paramètres et confidentialité</Text>

        <Card>
          <Text style={styles.label}>Serveur API</Text>
          <Text style={styles.value}>{API_URL}</Text>
          <Text style={styles.muted}>
            Adresse publique lue depuis EXPO_PUBLIC_API_URL. Aucun secret n'est embarqué.
          </Text>
        </Card>

        <Card>
          <Text style={styles.label}>Analyse</Text>
          <Text style={styles.muted}>
            L'analyse est passive : le serveur ne visite jamais les liens soumis. Les résultats
            sont indicatifs et n'accusent personne.
          </Text>
        </Card>

        <Card>
          <Text style={styles.label}>Données</Text>
          <Text style={styles.muted}>
            Les contacts signalés sont hachés. Les analyses conservent un extrait limité et un
            hachage. Le jeton de connexion est stocké dans le coffre sécurisé de l'appareil.
          </Text>
          <Text onPress={() => void clearToken()} style={styles.action}>
            Effacer le jeton local
          </Text>
        </Card>

        <Link href="/report" style={styles.link}>Signaler un contact</Link>
        <Link href="/login" style={styles.link}>Se connecter</Link>

        <Disclaimer>
          Un risque faible n'est jamais une garantie de sécurité. SAFECLICK ne remplace pas
          les vérifications auprès des organisations officielles.
        </Disclaimer>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: COLORS.night },
  content: { padding: 20, paddingBottom: 40 },
  title: { color: COLORS.text, fontSize: 26, fontWeight: "800" },
  label: { color: COLORS.text, fontSize: 14, fontWeight: "700" },
  value: { color: COLORS.electric, fontSize: 12, marginTop: 6 },
  muted: { color: COLORS.muted, fontSize: 12, lineHeight: 18, marginTop: 8 },
  action: { color: COLORS.electric, fontSize: 13, marginTop: 14 },
  link: { color: COLORS.electric, fontSize: 14, marginTop: 16 },
});
