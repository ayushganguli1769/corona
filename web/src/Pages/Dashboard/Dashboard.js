import React, { Component, useState, useEffect } from 'react'
import Graph from './Graph';
import Map from '../../Components/Map/Map'
import './styles.css';
export default class Dashboard extends Component {
  constructor(props) {
    super(props)
    this.state = {
      data: [],
      index: '',
      act: 0
    }

  }
  async fetchAPI() {
    fetch("https://api.covid19india.org/data.json")
      .then(res => res.json())
      .then(res =>
        this.setState({
          data: res.statewise
        }))
      .catch(err => console.log(err))
  }
  componentDidMount() {
    this.fetchAPI();
  }
  render() {
    var datas = this.state.data
    return (
      <div style={{ paddingTop: "20px" }} className="container">
        <Map />
        <h1 className="text-center">Coronavirus stats (India)</h1>
        <Graph />
        <br/>
          <br/>
        <div className="scrollable">
          <table className="table" >
            <thead className="thead-dark ">
              <tr>
                <th scope="col">#</th>
                <th scope="col">States</th>
                <th scope="col">Active</th>
                <th scope="col">Confirmed</th>
                <th scope="col">Deaths</th>
              </tr>
            </thead>
            <tbody>
              {datas.map((event, index) => (
                <tr key={index + 1}>
                  <th scope="row">{index + 1}</th>
                  <td>{event.state}</td>
                  <td>{event.active}</td>
                  <td>{event.confirmed}</td>
                  <td>{event.deaths}</td>
                </tr>
              ))}
            </tbody>
          </table>
          
        </div>
        <br/>
        <br/>
      </div>
    )
  }
}