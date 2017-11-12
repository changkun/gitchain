import React, { Component } from 'react';
import { Text, View, StyleSheet, ScrollView } from 'react-native';
import { Constants } from 'expo';

// You can import from local files
import Currency from './components/Currency';

// or any pure javascript modules available in npm
import { Card } from 'react-native-elements'; // 0.17.0

export default class App extends Component {
  render() {
    return (
      <View>
      <Text style={styles.title}>GitChain HotList:</Text>
      <ScrollView>
        <Card>
          <Currency />
        </Card>
        <Card>
          <Currency />
        </Card>
        <Card>
          <Currency />
        </Card>
        <Card>
          <Currency />
        </Card>
        <Card>
          <Currency />
        </Card>
        <Card>
          <Currency />
        </Card>
        <Card>
          <Currency />
        </Card>
        <Card>
          <Currency />
        </Card>
        <Card>
          <Currency />
        </Card>
        <Card>
          <Currency />
        </Card>
      </ScrollView>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'flex-start',
    paddingTop: Constants.statusBarHeight,
    backgroundColor: '#ecf0f1'
  },
  title: {
    marginTop: 24,
    fontSize: 18,
    fontWeight: 'bold',
    textAlign: 'center',
  },
});
