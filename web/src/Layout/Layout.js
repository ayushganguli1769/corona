import React from "react";
import {Route,Switch,withRouter,} from "react-router-dom";
import Header from "../Components/Header/Header";
import Sidebar from "../Components/Sidebar/Sidebar";
import Dashboard from "../Pages/Dashboard/Dashboard";
import Register from "../Pages/Register/Register";
import Profiles from "../Pages/Profiles/Profiles"

function Layout(props) {

  return (
    <div >
        <Header history={props.history} />
        <div style={{display:"flex"}}>
          <Sidebar />
          <Switch>
            <Route path="/app/dashboard" component={Dashboard} />
            <Route path="/app/register" component={Register} />
            <Route path="/app/profiles" component={Profiles} />
          </Switch>
        </div>
    </div>
  );
}

export default withRouter(Layout);