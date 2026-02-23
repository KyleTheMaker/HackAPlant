import { Text, View } from "react-native";
import useDeviceData from "@/utilities/monitorServerClient";

export default function Index() {
  const deviceData = useDeviceData();
  return (
    <View
      style={{
        flex: 1,
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <Text>Temperature: { deviceData? deviceData?.temperature : "Loading Data..."}</Text>
      <Text>Moisture: { deviceData? deviceData?.moisture : "Loading Data..."}</Text>
    </View>
  );
}
