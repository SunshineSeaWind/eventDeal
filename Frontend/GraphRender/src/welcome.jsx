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
                      href='#/galaxy/OfficialTimelineTimeNodeConnect?cx=-7581&cy=-615&cz=6765&lx=0.0332&ly=-0.4439&lz=0.0229&lw=0.8952&ml=150&s=1.75&l=1&v=2018-3-7T00-00-00Z'
                      media='composer_fly_first.png'
                      name='OfficialTimeline'/>
          <Destination description='TestGraphTest'
                      href='#/galaxy/TestGraphTest?l=1'
                      media='composer_fly_first.png'
                      name='TestGraphTest'/>
          <Destination description='UnofficialRelations'
                          href='#/galaxy/UnofficialRelations?cx=-4114&cy=-4044&cz=1837&lx=0.3022&ly=-0.8714&lz=0.3848&lw=0.0360&ml=150&s=1.75&l=1&v=2018-2-20T00-00-00Z'
                          media='composer_fly_first.png'
                          name='UnofficialRelations'/>
          <Destination description='UnofficialTimeline'
                          href='#/galaxy/UnofficialTimeline?cx=350&cy=653&cz=-15875&lx=0.1818&ly=-0.9793&lz=0.0712&lw=0.0532&ml=150&s=1.75&l=1&v=2018-2-20T00-00-00Z'
                          media='composer_fly_first.png'
                          name='UnofficialTimeline'/>
			
        </div>
      </div>
    );
  }
}
