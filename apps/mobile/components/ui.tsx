import type { ReactNode } from "react";
import { Pressable, StyleSheet, Text, View } from "react-native";
import { COLORS } from "@/constants/theme";

export function PrimaryButton({
  label,
  onPress,
  disabled = false,
}: {
  label: string;
  onPress: () => void;
  disabled?: boolean;
}) {
  return (
    <Pressable
      onPress={onPress}
      disabled={disabled}
      style={({ pressed }) => [
        styles.button,
        disabled && styles.buttonDisabled,
        pressed && styles.buttonPressed,
      ]}
    >
      <Text style={styles.buttonText}>{label}</Text>
    </Pressable>
  );
}

export function Card({ children }: { children: ReactNode }) {
  return <View style={styles.card}>{children}</View>;
}

export function ErrorText({ message }: { message: string }) {
  if (!message) return null;
  return <Text style={styles.error}>{message}</Text>;
}

export function Disclaimer({ children }: { children: ReactNode }) {
  return <Text style={styles.disclaimer}>{children}</Text>;
}

const styles = StyleSheet.create({
  button: {
    backgroundColor: COLORS.electric,
    borderRadius: 12,
    paddingVertical: 14,
    alignItems: "center",
    marginTop: 14,
  },
  buttonDisabled: { opacity: 0.5 },
  buttonPressed: { opacity: 0.8 },
  buttonText: { color: "#ffffff", fontSize: 15, fontWeight: "700" },
  card: {
    backgroundColor: COLORS.surface,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: "rgba(255,255,255,0.1)",
    padding: 18,
    marginTop: 16,
  },
  error: {
    color: "#fca5a5",
    fontSize: 13,
    lineHeight: 19,
    marginTop: 12,
  },
  disclaimer: { color: COLORS.muted, fontSize: 12, lineHeight: 18, marginTop: 20 },
});
