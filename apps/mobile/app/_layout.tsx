import { Stack } from "expo-router";
import { StatusBar } from "expo-status-bar";
import { COLORS } from "@/constants/theme";

export default function RootLayout() {
  return (
    <>
      <Stack
        screenOptions={{
          headerStyle: { backgroundColor: COLORS.night },
          headerTintColor: COLORS.text,
          contentStyle: { backgroundColor: COLORS.night },
        }}
      />
      <StatusBar style="light" />
    </>
  );
}
