import React from 'react';

class Map extends React.Component {
    render() {
        return (
            <div className="container ">
                <h1 className="text-center">Map</h1>
                <div className="row  justify-content-center align-items-center">
                    <div id="visualization" style={{ margin: "1em" }}> </div>
                    </div>
            </div>
        );
    }
}
export default Map;