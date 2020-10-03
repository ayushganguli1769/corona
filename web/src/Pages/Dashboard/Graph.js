import React, { Component, useState, useEffect } from 'react'
import { Line } from 'react-chartjs-2';

export default class Graph extends Component {
    constructor(props) {
        super(props)
        this.state = {
            labels: [],
            datasets: [
                {
                    label: 'Affected',
                    fill: true,
                    data: []
                }
            ]
        }
        //this.state = state;
    }
    async fetchAPI() {
        fetch("https://api.covid19india.org/data.json")
            .then(res =>
                res.json())
            .then(res => {
                var l = [];
                res.cases_time_series.forEach(ele => l.push(ele.date));
                var t = [];
                res.cases_time_series.forEach(ele => t.push(ele.totalconfirmed));
                // console.log(l);
                // console.log(t);
                this.setState({
                    labels: l,
                    datasets: [
                        {
                            label: 'Affected',
                    fill: true,
                   
                   
                    data: t,
                        }
                    ]
                })}
        )
        .catch(err => console.log(err))
    }

componentDidMount(){
    this.fetchAPI();
}
render() {
    var datas = this.state;
    // console.log(datas)
    return (
        <div>
            <Line
          data={datas}
          options={{
            title:{
              display:true,
              text:'Affected',
              fontSize:20
            },
            legend:{
              display:true,
              position:'right'
            }
          }}
        />
        </div>
    )
}
}
