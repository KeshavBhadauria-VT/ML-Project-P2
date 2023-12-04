import logo from './logo.svg';
import './App.css';
import MainPage from './components/MainPage';
import MyNavbar from './components/Navbar';

function App() {
  return (
    <div className="App">
      <MyNavbar></MyNavbar>
      <MainPage></MainPage>
    </div>
  );
}

export default App;
