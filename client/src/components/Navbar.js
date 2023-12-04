import React from "react"
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';


const MyNavbar = (props) => {
  return (
    <div>
    <Navbar expand="lg" className="bg-body-tertiary">
      <Container>
        <Navbar.Brand href="#home">Team 10</Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
      </Container>
    </Navbar>
    </div>
  )
};

export default MyNavbar;
