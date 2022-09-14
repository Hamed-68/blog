import SignIn from './Auth/SignIn/SignIn'
import LogIn from './Auth/LogIn/LogIn'
import Main from './Components/Main'
import NotFound from './Components/NotFound/NotFound';
import UserNotFound from './Components/NotFound/UserNotFound'
import { Switch, Route, Redirect } from 'react-router-dom';
import './App.css';
import UserProfile from './Components/UserProfile'

function App() {
  return (
    <Switch>
      <Route path='/signin' component={SignIn} />
      <Route path='/login' component={LogIn} />
      <Route path='/blog' component={Main} />
      <Route path='/users/:user' component={UserProfile} />
      <Route path='/usernotfound' component={UserNotFound} />
      <Redirect exact from='/' to='/login' />
      <Route path='*' component={NotFound} />
    </Switch>
  );
}

export default App;
