import React from "react";
import Destination from './destination.jsx';

export default class WelcomePage extends React.Component {
  render() {
    return (
      <div className='container'>
        <h1>Welcome to the Code Galaxies, Commander</h1>
        <h2>Choose your destination:</h2>
        <div className='media-list'>
          <Destination description='Relations'
                      href='#/galaxy/Relations?cx=-1&cy=0&cz=177&lx=0.0000&ly=0.0000&lz=0.0000&lw=1.0000&ml=150&s=1.75&l=1'
                      media='brew_fly_first.png'
                      name='Relations'/>
          <Destination description='Timeline'
                      href='#/galaxy/Timeline?l=1'
                      media='composer_fly_first.png'
                      name='Timeline'/>
        </div>
      </div>
    );
  }
}
