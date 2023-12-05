import React from "react"
import { Typeahead } from 'react-bootstrap-typeahead';
import 'react-bootstrap-typeahead/css/Typeahead.css';
import { useState, useEffect } from "react";
import {Container, Row, Col} from "react-bootstrap"
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';

const MainPage = (props) => {
    // Sample data for the autocomplete


    const [selectedOption, setSelectedOption] = useState([]);

    const [players, setPlayers] = useState([]);

    const [playerSelectedList, setPlayerSelectedList] = useState([]);

    const [selectedOption2, setSelectedOption2] = useState([]);
    
    const [playerSelectedList2, setPlayerSelectedList2] = useState([]);

    const [predictedScore, setPredictedScore] = useState(0);

    const [predictedScore2, setPredictedScore2] = useState(0);

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
        //use api call
        if (playerSelectedList.length !== 0) {
            setPredictedScore((prev) => prev + Math.floor(Math.random() * (100 - 3 + 1)) + 3);
        }
    }, [playerSelectedList])

    useEffect(() => {
        //use api call
        if (playerSelectedList2.length !== 0) {
            setPredictedScore2((prev) => prev + Math.floor(Math.random() * (100 - 3 + 1)) + 3);
        }
    }, [playerSelectedList2])



    return (

        <Container>
            <Row>
                <Col md={{ span: 2, }}>
                    <Typeahead
                        style={{paddingTop: 20}}
                        id="myTypeahead"
                        labelKey={(option) => `${option.full_name}`} // Adjust this based on the structure of your data
                        options={players}
                        placeholder="Enter a player"
                        selected={selectedOption}
                        onChange={selected => {setSelectedOption(selected); setPlayerSelectedList((prev) => [...prev, ...selected]);}}
                        // 
                        />
                    
                    <h6 style={{paddingTop: 250}}>Predicted Fanstasy Points</h6>
                    <h3 style={{textAlign: "center"}}>{predictedScore}</h3>
                    
                </Col>
                <Col md={{span: 3, offset: 0}} className="center-block">
                    {playerSelectedList.map((item) => 
                        <div className="text-center mx-auto">
                            <Card style={{ width: '18rem', marginLeft: "auto", marginRight: "auto" }}>
                                <Card.Img variant="top"  src={`https://cdn.nba.com/headshots/nba/latest/260x190/${item.id}.png`} />
                                <Card.Body>
                                    <Card.Title>{item.full_name}</Card.Title>
                                </Card.Body>
                            </Card>
                        </div>
                    )}
                </Col>

                <Col md={{span: 2}} className="text-center">
                    <Button className="text-center">Calculate!</Button>
                
                </Col>

                <Col md={{span: 3, offset: 0}} className="center-block">
                    {playerSelectedList2.map((item) => 
                        <div className="text-center mx-auto">
                            <Card style={{ width: '18rem', marginLeft: "auto", marginRight: "auto" }}>
                                <Card.Img variant="top"  src={`https://cdn.nba.com/headshots/nba/latest/260x190/${item.id}.png`} />
                                <Card.Body>
                                    <Card.Title>{item.full_name}</Card.Title>
                                </Card.Body>
                            </Card>
                        </div>
                    )}
                </Col>

                <Col md={{ span: 2 }}>
                    <Typeahead
                        style={{paddingTop: 20}}
                        id="myTypeahead"
                        labelKey={(option) => `${option.full_name}`} // Adjust this based on the structure of your data
                        options={players}
                        placeholder="Enter a player"
                        selected={selectedOption2}
                        onChange={selected => {setSelectedOption2(selected); setPlayerSelectedList2((prev) => [...prev, ...selected]);}}
                        // 
                        />

                    <h6 style={{paddingTop: 250}}>Predicted Fanstasy Points</h6>
                    <h3 style={{textAlign: "center"}}>{predictedScore2}</h3>
                </Col>
                
            </Row>
        </Container>
    );
};

export default MainPage;
