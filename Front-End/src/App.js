import SignIn from './Auth/SignIn/SignIn'
import LogIn from './Auth/LogIn/LogIn'
import Main from './Components/Main'
import NotFound from './Components/NotFound/NotFound';
import { Switch, Route, Redirect } from 'react-router-dom';
import './App.css';

function App() {
  return (
    <Switch>
      <Route path='/signin' component={SignIn} />
      <Route path='/login' component={LogIn} />
      <Route path='/blog' component={Main} />
      <Redirect exact from='/' to='/login' />
      <Route path='*' component={NotFound} />
    </Switch>
  );
}

export default App;
