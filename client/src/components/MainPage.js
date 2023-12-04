import React from "react"
import { Typeahead } from 'react-bootstrap-typeahead';
import 'react-bootstrap-typeahead/css/Typeahead.css';
import { useState, useEffect } from "react";
import {Container, Row, Col} from "react-bootstrap"

const MainPage = (props) => {
    // Sample data for the autocomplete


    const [selectedOption, setSelectedOption] = useState([]);

    const [players, setPlayers] = useState([]);

    const [playerSelectedList, setPlayerSelectedList] = useState([]);


    useEffect(() => {
      const fetchPlayers = async () => {
        try {
          const response = await fetch('http://localhost:4000/api/get_players');
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
  
          const data = await response.json();
          setPlayers(data.data);
          const playerNames = await data.data.map(item => item.full_name);
        } catch (error) {
          console.error('Error fetching players:', error.message);
        }
      };
  
      fetchPlayers();
    }, []); // Empty dependency array ensures that the effect runs once after the component mounts

    useEffect(() => {
        
    })
    return (

        <Container>
            <Row>
                <Col md={{span: 6, offset: 3}}>
                    {playerSelectedList.map((item) => <p>{item.full_name}</p>)}
                </Col>

                <Col md={{ span: 6, offset: 3 }}>
                    <Typeahead
                        style={{paddingTop: 20}}
                        id="myTypeahead"
                        labelKey={(option) => `${option.full_name}`} // Adjust this based on the structure of your data
                        options={players}
                        placeholder="Enter a player"
                        selected={selectedOption}
                        onChange={selected => {setSelectedOption(selected); setPlayerSelectedList((prev) => [...prev, selected])}}
                        // 
                        />
                </Col>
            </Row>
        </Container>
    );
};

export default MainPage;
