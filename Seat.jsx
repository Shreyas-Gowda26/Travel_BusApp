import React from "react";
import { TouchableOpacity, Text, StyleSheet } from "react-native";

export default function Seat({ seat, onPress }) {
  return (
    <TouchableOpacity
      style={[
        styles.seat,
        seat.seat_status === "booked" ? styles.bookedSeat : styles.availableSeat,
      ]}
      onPress={() => onPress(seat)}
    >
      <Text style={styles.seatText}>{seat.seat_number}</Text>
    </TouchableOpacity>
  );
}

const styles = StyleSheet.create({
  seat: {
    width: 55,
    height: 55,
    borderRadius: 10,
    margin: 10,
    justifyContent: "center",
    alignItems: "center",
  },
  availableSeat: {
    backgroundColor: "green",
  },
  bookedSeat: {
    backgroundColor: "red",
  },
  seatText: {
    color: "#fff",
    fontSize: 16,
    fontWeight: "600",
  },
});
