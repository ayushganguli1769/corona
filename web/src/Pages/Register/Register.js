import React, { Component } from 'react'
import axios from 'axios';

export default class Register extends Component {
  constructor() {
    super();
    this.state = {
      username: '',
      contact: '',
      email: '',
      status:'',
      latitude:'',
      longitude:'',
      password:'12345678'
    };
  }
  onChange = (e) => {
    this.setState({ [e.target.name]: e.target.value });
  }
  onSubmit = (e) => {
    e.preventDefault();
    const { username, contact, email,status,latitude,longitude,password } = this.state;
    axios.post('http://tuhina840.pythonanywhere.com//tracker/admin_add_user_detail/', { username, contact, email,status,latitude,longitude,password })
      .then((result) => {
        console.log(result);
        console.log(result.data);
      });
  }
    render() {
      const {  username, contact, email,status,latitude,longitude,password  } = this.state;
        return (
            <form onSubmit={this.handleSubmit} style={{width:"100vw", paddingLeft:"20vw",paddingRight:"20vw",color:"black",paddingTop:"10vh"}}>
            <h1>Register</h1><br/>
            <div class="form-group">
    <label for="name1" >Name</label>
    <input type="text" class="form-control" id="name1" placeholder="Enter Name"type="text" name="username" value={username} onChange={this.onChange}/>
  </div>
  <div class="form-group">
    <label for="email1" >Email address</label>
    <input type="email" class="form-control" id="email1" placeholder="name@example.com" type="text" name="email" value={email} onChange={this.onChange}/>
  </div>
  <div class="form-group">
    <label for="contact1" >Contact</label>
    <input type="number" class="form-control" id="contact1" placeholder="Enter Contact" type="text" name="contact" value={contact} onChange={this.onChange}/>
  </div>
  <div class="form-group">
    <label for="Select1" >Status</label>
    <select class="form-control" id="Select1" type="text" name="status" value={status} onChange={this.onChange}>
      <option value="1">1. Corona Virus Positive</option>
      <option value="2">2.Shows Symtoms</option>
      <option value="3">3. Travel History Abroad</option>
      <option value="4">4. Close Contact</option>
      <option value="5">5. Normal User</option>
    </select>
  </div>
  <div class="form-group" style={{display:"none"}}>
    <label for="lat1" >Password</label>
    <input type="string" class="form-control" id="lat1" placeholder="Enter Latitude" type="text" name="password" value="12345678" onChange={this.onChange}/>
  </div>
  <div class="form-group">
    <label for="lat1" >Latitude</label>
    <input type="string" class="form-control" id="lat1" placeholder="Enter Latitude" type="text" name="latitude" value={latitude} onChange={this.onChange}/>
  </div>
  <div class="form-group">
    <label for="long1">Longitude</label>
    <input type="string" class="form-control" id="long1" placeholder="Enter Longitude" type="text" name="longitude" value={longitude} onChange={this.onChange}/>
  </div>
  <button class="btn-primary" type="submit">Submit</button>
</form>
        )
    }
}
