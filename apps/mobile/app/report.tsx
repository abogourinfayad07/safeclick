import { useState } from "react";
import { ScrollView, StyleSheet, Text, TextInput, View } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { Card, ErrorText, PrimaryButton } from "@/components/ui";
import { COLORS } from "@/constants/theme";
import { api, errorMessage } from "@/lib/api";

const kinds = ["email", "phone", "url", "other"] as const;
const reasons = ["urgency", "payment_request", "code_request", "impersonation", "other"] as const;

export default function ReportScreen() {
  const [contactKind, setContactKind] = useState<(typeof kinds)[number]>("email");
  const [contact, setContact] = useState("");
  const [reason, setReason] = useState<(typeof reasons)[number]>("urgency");
  const [acknowledged, setAcknowledged] = useState(false);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function submit() {
    setNotice("");
    setError("");
    setLoading(true);
    try {
      const response = await api.createReport({
        contact_kind: contactKind,
        contact,
        reason_code: reason,
        acknowledge_unverified: true,
      });
      setNotice(response.message);
      setContact("");
      setAcknowledged(false);
    } catch (cause) {
      setError(errorMessage(cause));
    } finally {
      setLoading(false);
    }
  }

  return (
    <SafeAreaView style={styles.safe} edges={["top"]}>
      <ScrollView contentContainerStyle={styles.content} keyboardShouldPersistTaps="handled">
        <Text style={styles.title}>Signaler un contact</Text>
        <Text style={styles.subtitle}>
          Le contact est haché avant stockage. Aucune accusation n'est faite automatiquement.
        </Text>

        <Card>
          <Text style={styles.label}>Type de contact</Text>
          <View style={styles.chips}>
            {kinds.map((item) => (
              <Text
                key={item}
                onPress={() => setContactKind(item)}
                style={[styles.chip, contactKind === item && styles.chipActive]}
              >
                {item}
              </Text>
            ))}
          </View>

          <Text style={[styles.label, { marginTop: 18 }]}>Motif</Text>
          <View style={styles.chips}>
            {reasons.map((item) => (
              <Text
                key={item}
                onPress={() => setReason(item)}
                style={[styles.chip, reason === item && styles.chipActive]}
              >
                {item}
              </Text>
            ))}
          </View>

          <Text style={[styles.label, { marginTop: 18 }]}>Contact</Text>
          <TextInput
            style={styles.input}
            value={contact}
            onChangeText={setContact}
            placeholder="Contact à signaler"
            placeholderTextColor={COLORS.muted}
            autoCapitalize="none"
            autoCorrect={false}
          />

          <Text
            onPress={() => setAcknowledged(!acknowledged)}
            style={[styles.ack, acknowledged && styles.ackActive]}
          >
            {acknowledged ? "☑ Je comprends qu'un signalement n'est pas une preuve." : "☐ Je comprends qu'un signalement n'est pas une preuve."}
          </Text>
        </Card>

        <PrimaryButton
          label={loading ? "Envoi…" : "Envoyer le signalement"}
          onPress={() => void submit()}
          disabled={loading || contact.trim().length < 3 || !acknowledged}
        />
        {notice ? <Text style={styles.notice}>{notice}</Text> : null}
        <ErrorText message={error} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: COLORS.night },
  content: { padding: 20, paddingBottom: 40 },
  title: { color: COLORS.text, fontSize: 26, fontWeight: "800" },
  subtitle: { color: COLORS.muted, fontSize: 14, lineHeight: 20, marginTop: 8 },
  label: { color: COLORS.text, fontSize: 13, fontWeight: "700" },
  chips: { flexDirection: "row", flexWrap: "wrap", gap: 8, marginTop: 10 },
  chip: {
    color: COLORS.muted,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.15)",
    borderRadius: 999,
    paddingHorizontal: 10,
    paddingVertical: 6,
    fontSize: 11,
  },
  chipActive: { color: "#ffffff", backgroundColor: COLORS.electric, borderColor: COLORS.electric },
  input: {
    backgroundColor: "rgba(0,0,0,0.25)",
    borderColor: "rgba(255,255,255,0.12)",
    borderWidth: 1,
    borderRadius: 10,
    color: COLORS.text,
    padding: 12,
    marginTop: 8,
    fontSize: 13,
  },
  ack: { color: COLORS.muted, fontSize: 12, lineHeight: 18, marginTop: 16 },
  ackActive: { color: "#86efac" },
  notice: { color: "#86efac", fontSize: 13, lineHeight: 19, marginTop: 14 },
});
