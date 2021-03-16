import React from 'react';
import {vibrate} from './utils';
import { StyleSheet, Text, View ,Button} from 'react-native';

const display = props=>{
  if(props.state.studyTimeflag){
    let min=Math.floor(props.state.studyTime/60)
    let sec=props.state.studyTime % 60
    return(<View>
      <Text>Study Time</Text>
      <Text>{min}:{sec} </Text>
      <Button onPress={props.onReset} title="reset"/>
      <Button onPress={props.onStop} title="pause" />
      <Button onPress={props.onStart} title="start" />
      </View>
  )

  }
}
export default class App extends React.Component {
  constructor(){
    super()
    this.state={
      studyTime:1500,
      breakTime:300,
      studyTimeflag:True,
      breaktimeflag:False,
      pause:False,
    }
  }

  componentDidMount(){
    if (!this.state.pause){
      if(this.state.studyTime > 0 || this.state.breakTime > 0){setInterval(this.reduce,1000)}
      else if (this.state.studyTime === 0) {
        this.setState({
          studyTimeflag:False,
          breaktimeflag:True,
          breakTime:300,
          studyTime:1500,
          pause:False,
        })
        vibrate()
      }
      else if (this.state.breakTime === 0) {
        this.setState({
          studyTimeflag:True,
          breaktimeflag:False,
          breakTime:300,
          studyTime:1500,
          pause:False,
        })
        vibrate()
      }

    }
  }
  onReset = ()=>{
    this.setState(
      {
        studyTime:1500,
        breakTime:300,
        studyTimeflag:True,
        breaktimeflag:False,
        pause:False,
      }
    )
  }
  onPause = ()=>{
    this.setState({
      pause:True
    })

  }
  onStart = ()=>{
    this.setState(prevState =>({
      this.state.pause=!prevState.pause
    })
  }

  reduce = ()=>{
    if(prevState.studyTimeflag){
      this.setState(prevState=>({studyTime:prevState.studyTime-1}))
    }
    else(){
      this.setState(prevState=>({studyTime:prevState.breakTime-1}))
    }

  }

  render() {
    return (
      <View style={styles.container}>
        <Display
        onReset={()=>this.onReset()}
        onStop={()=>this.onPause()}
        onStart={()=>this.onStart()}
        state={this.state}
        />
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
