import React from "react"
import { Typeahead } from 'react-bootstrap-typeahead';
import 'react-bootstrap-typeahead/css/Typeahead.css';
import { useState, useEffect } from "react";
import {Container, Row, Col, Button} from "react-bootstrap"
import Tab from 'react-bootstrap/Tab';
import Tabs from 'react-bootstrap/Tabs';
import Card from 'react-bootstrap/Card';


const MainPage = (props) => {
    // Sample data for the autocomplete


    const [selectedOption, setSelectedOption] = useState([]);

    const [players, setPlayers] = useState([]);

    const [playerSelectedList, setPlayerSelectedList] = useState([]);

    const [selectedOption2, setSelectedOption2] = useState([]);
    
    const [selectedOption3, setSelectedOption3] = useState([]);

    const [selectedOption4, setSelectedOption4] = useState([]);
    
    const [playerSelectedList2, setPlayerSelectedList2] = useState([]);

    const [predictedScore, setPredictedScore] = useState(0);

    const [predictedScore2, setPredictedScore2] = useState(0);

    const [teams, setTeams] = useState([]);

    const [teamSelectedList, setTeamSelectedList] = useState([]);

    const [teamSelectedList2, setTeamSelectedList2] = useState([]);

    const [outlineCard, setOutlineCard] = useState("");

    const [outlineCard2, setOutlineCard2] = useState("");

    useEffect(() => {
      const fetchPlayers = async () => {
        try {
          const response = await fetch('http://localhost:4000/api/get_players');
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }
  
          const data = await response.json();
          setPlayers(data.data);
        } catch (error) {
          console.error('Error fetching players:', error.message);
        }
      };
      const fetchTeams = async () => {
        try {
          const response = await fetch('http://localhost:4000/api/get_team');
          if (!response.ok) {
            throw new Error('Network response was not ok');
          }

          const data = await response.json();
          setTeams(data.data);
        } catch (error) {
          console.error('Error fetching players:', error.message)
        }
      }
  
      fetchPlayers();
      fetchTeams();
    }, []); // Empty dependency array ensures that the effect runs once after the component mounts

    useEffect(() => {
        //use api call
        if (playerSelectedList.length !== 0) {
            fetch(`http://localhost:4000/api/get_prediction/${playerSelectedList[playerSelectedList.length - 1]["full_name"]}`, {
            method: "GET"
            })
            .then(response => {
                if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // Handle the JSON response
                console.log(data);
                setPredictedScore((prev) => Math.round(prev + data.data));
                setPlayerSelectedList(playerSelectedList.map((item,i)=>{
                    if(playerSelectedList.length === i - 1){
                      return {...item, predictedPoints: data.data};
                    }
                    return item;
                  }))  
                  console.log(playerSelectedList);              
            })
            .catch(error => {
                // Handle errors
                console.error("Fetch error:", error);
            });
            
        }
    }, [playerSelectedList.length])

    useEffect(() => {
        if (playerSelectedList2.length !== 0) {
            fetch(`http://localhost:4000/api/get_prediction/${playerSelectedList2[playerSelectedList2.length - 1]["full_name"]}`, {
            method: "GET"
            })
            .then(response => {
                if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                // Handle the JSON response
                console.log(data);
                setPredictedScore2((prev) => Math.round(prev + data.data));           
            })
            .catch(error => {
                // Handle errors
                console.error("Fetch error:", error);
            });
            
        }
    }, [playerSelectedList2.length])


    function calculate_whatever() {
        if (Math.random() < 0.5) {
            setOutlineCard("danger");
            setOutlineCard2("success");
        } else {
            setOutlineCard("success");
            setOutlineCard2("danger");
        }
    }

    return (

        <Container>
            <Tabs
                defaultActiveKey="home"
                id="uncontrolled-tab-example"
                className="mb-3">
                
                <Tab eventKey="home" title="Home">
                    <Row style={{paddingTop: 45}}>
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
                            <h3>Calculate!</h3>
                        
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
                </Tab>








                <Tab eventKey="Games" title="Games">
                    <Row style={{paddingTop: 45}}>
                        <Col md={{ span: 2, }}>
                            <Typeahead
                                style={{paddingTop: 20}}
                                id="whatever"
                                labelKey={(option) => `${option.full_name}`} // Adjust this based on the structure of your data
                                options={teams}
                                placeholder="Enter a Team"
                                selected={selectedOption3}
                                onChange={selected => {setSelectedOption3(selected); setTeamSelectedList((prev) => [...prev, ...selected]);}}
                                // 
                                />

                            {outlineCard2 ? outlineCard2 === "success" ? <h3 style={{textAlign: "center", paddingTop: 100}}>WINNER!</h3> : <h3 style={{textAlign: "center", paddingTop: 100}}>LOSER!</h3> : <></>}
                            
                        </Col>
                        <Col md={{span: 3, offset: 0}} className="center-block">
                        <h3 style={{textAlign: "center"}}>Home</h3>
                            {teamSelectedList.map((item) => 
                                <div className="text-center mx-auto">
                                    <Card border={outlineCard2} style={{ width: '18rem', marginLeft: "auto", marginRight: "auto" }}>
                                        <Card.Img variant="top"  src={`https://cdn.nba.com/logos/nba/${item.id}/primary/L/logo.svg`} />
                                        <Card.Body>
                                            <Card.Title>{item.full_name}</Card.Title>
                                        </Card.Body>
                                    </Card>
                                </div>
                            )}
                        </Col>

                        <Col md={{span: 2}} className="text-center">
                            {teamSelectedList2.map((item) => <Button variant="success" size="lg" onClick={calculate_whatever}>Calculate!</Button>)}
                        </Col>

                        <Col md={{span: 3, offset: 0}} className="center-block">
                            <h3 style={{textAlign: "center"}}>Away</h3>
                            {teamSelectedList2.map((item) => 
                                <div className="text-center mx-auto">
        
                                    <Card border={outlineCard}  style={{ width: '18rem', marginLeft: "auto", marginRight: "auto" }}>
                                        <Card.Img variant="top"  src={`https://cdn.nba.com/logos/nba/${item.id}/primary/L/logo.svg`} />
                                        <Card.Body>
                                            <Card.Title>{item.full_name}</Card.Title>
                                        </Card.Body>
                                    </Card>
                                </div>
                            )}
                        </Col>
                        <Col md={{ span: 2, }}>
                            <Typeahead
                                style={{paddingTop: 20}}
                                id="whatever"
                                labelKey={(option) => `${option.full_name}`} // Adjust this based on the structure of your data
                                options={teams}
                                placeholder="Enter a Team"
                                selected={selectedOption4}
                                onChange={selected => {setSelectedOption4(selected); setTeamSelectedList2((prev) => [...prev, ...selected]);}}
                                // 
                                />
                            {outlineCard ? outlineCard === "success" ? <h3 style={{textAlign: "center", paddingTop: 100}}>WINNER!</h3> : <h3 style={{textAlign: "center", paddingTop: 100}}>LOSER!</h3> : <></>}

                        </Col>

                    </Row>
                </Tab>

            </Tabs>

        </Container>
    );
};

export default MainPage;
