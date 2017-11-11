import React, { Component } from 'react';
import { Text, View, StyleSheet, Image } from 'react-native';

export default class Currency extends Component {
  render() {
    return (
      <View style={styles.container}>
        <Text style={styles.paragraph}>
          Bitcoin Performance
        </Text>
        <Image style={styles.positive} source={require("../assets/good2.png")}/>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    justifyContent: 'space-between',
    flexDirection: 'row',
    width: 300
  },
  paragraph: {
    fontSize: 14,
    fontWeight: 'bold',
    textAlign: 'center',
    color: '#34495e',
    marginTop: 10
  },
  positive: {
    backgroundColor: "#38E09D",
    height: 40,
    width: 40
  },
  negative: {
    backgroundColor: "#F23349",
    height: 40,
    width: 40
  }
});
