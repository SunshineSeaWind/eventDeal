import React from "react";
import Destination from './destination.jsx';

export default class WelcomePage extends React.Component {
  render() {
    return (
      <div className='container'>
        <h1>Welcome to the Code Galaxies, Commander</h1>
        <h2>Choose your destination:</h2>
        <div className='media-list'>
          <Destination description='OfficialRelations'
                      href='#/galaxy/OfficialRelations?cx=-1&cy=0&cz=177&lx=0.0000&ly=0.0000&lz=0.0000&lw=1.0000&ml=150&s=1.75&l=1'
                      media='brew_fly_first.png'
                      name='OfficialRelations'/>
					  {/*<Destination description='OfficialTimeline'
                      href='#/galaxy/OfficialTimeline?l=1'
                      media='composer_fly_first.png'
                      name='OfficialTimeline'/>
          <Destination description='OfficialTimelineAddData'
                      href='#/galaxy/OfficialTimelineAddData?l=1'
                      media='composer_fly_first.png'
                      name='OfficialTimelineAddData'/>
					  */}
          <Destination description='OfficialTimelineTimeNodeConnect'
                      href='#/galaxy/OfficialTimelineTimeNodeConnect?cx=268&cy=0&cz=10485&lx=0.0000&ly=0.0000&lz=0.0000&lw=1.0000&ml=150&s=1.75&l=1&v=2018-3-7T00-00-00Z'
                      media='composer_fly_first.png'
                      name='OfficialTimeline'/>
          <Destination description='TestGraphTest'
                      href='#/galaxy/TestGraphTest?l=1'
                      media='composer_fly_first.png'
                      name='TestGraphTest'/>
          <Destination description='UnofficialRelations'
                          href='#/galaxy/UnofficialRelations?l=1'
                          media='composer_fly_first.png'
                          name='UnofficialRelations'/>
          <Destination description='UnofficialTimeline'
                          href='#/galaxy/UnofficialTimeline?l=1'
                          media='composer_fly_first.png'
                          name='UnofficialTimeline'/>

        </div>
      </div>
    );
  }
}
