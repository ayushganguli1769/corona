import React, { Component } from 'react'
import { compose } from "recompose"
import {withScriptjs,withGoogleMap,GoogleMap,Marker,InfoWindow} from "react-google-maps"


const MapWithAMarker = compose(withScriptjs, withGoogleMap)(props => {

  return (
    <GoogleMap defaultZoom={8} defaultCenter={{ lat: 29.5, lng: -95 }}>
      {props.markers.map(marker => {
        const onClick = props.onClick.bind(this, marker)
        return (
          <Marker
            key={marker.id}
            onClick={onClick}
            position={{ lat: marker.latitude, lng: marker.longitude }}
          >
            {props.selectedMarker === marker &&
              <InfoWindow>
                <div>
                  {marker.shelter}
                </div>
              </InfoWindow>}
          </Marker>
        )
      })}
    </GoogleMap>
  )
})
export default class Profiles extends Component {
    constructor(props) {
      super(props)
    
      this.state = {
         searched : false,
         location : false,
         shelters: [],
         selectedMarker: false
      }
    }

    componentDidMount() {
      fetch("https://api.harveyneeds.org/api/v1/shelters?limit=20")
        .then(r => r.json())
        .then(data => {
          this.setState({ shelters: data.shelters })
        })
    }

    handleClick = (marker, event) => {
      this.setState({ selectedMarker: marker })
    }
    
    render() {
        return (
            <div style={{paddingTop:"20px"}} className="container">
                <div class="input-group mb-3">
                  <input type="text" class="form-control" placeholder="Name" aria-label="Name" aria-describedby="button-addon2" />
                  <div class="input-group-append">
                    <button class="btn btn-outline-secondary" onClick={() => {
                      this.setState({
                        searched:true
                      })
                    }} type="button" id="button-addon2">Search</button>
                  </div>
                </div>
                {
                  (this.state.searched) ? 
                  <table class="table">
                  <thead class="thead-dark">
                    <tr>
                      <th scope="col">Number</th>
                      <th scope="col">Name</th>
                      <th scope="col">District</th>
                      <th scope="col">State</th>
                      <th scope="col">Status</th>
                      <th scope="col">Show Location</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <th scope="row">1</th>
                      <td>Ayush Ganguly</td>
                      <td>Korba</td>
                      <td>Chattishgarh</td>
                      <td>Positive</td>
                      <td><button type="button" onClick={() => {this.setState({location:true})}} class="btn btn-link">Show</button></td>
                    </tr>
                    <tr>
                    <th scope="row">2</th>
                      <td>Ayush Verma</td>
                      <td>Raipur</td>
                      <td>Chattishgarh</td>
                      <td>Positive</td>
                      <td><button type="button" onClick={() => {this.setState({location:true})}} class="btn btn-link">Show</button></td>
                    </tr>
                    <tr>
                    <th scope="row">3</th>
                      <td>Ayush Sarkar</td>
                      <td>Bhopal</td>
                      <td>Madhya Pradesh</td>
                      <td>Negative</td>
                      <td><button type="button" onClick={() => {this.setState({location:true})}} class="btn btn-link">Show</button></td>
                    </tr>
                  </tbody>
                </table>
                :
                  null
                }
                {
                  this.state.location ? 
                  <MapWithAMarker
                  selectedMarker={this.state.selectedMarker}
                  markers={this.state.shelters}
                  onClick={this.handleClick}
                  googleMapURL="https://maps.googleapis.com/maps/api/js?v=3.exp&libraries=geometry,drawing,places"
                  loadingElement={<div style={{ height: `100%` }} />}
                  containerElement={<div style={{ height: `400px` }} />}
                  mapElement={<div style={{ height: `100%` }} />}
                /> :
                null
                }
            </div>
        )
    }
}
