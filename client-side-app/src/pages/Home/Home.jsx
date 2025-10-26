import styles from './Home.module.css';
import Button from '../../components/Button/Button';
import { useState } from 'react';
import LostItemForm from '../LostItemForm/LostItemForm';
import FoundItemForm from '../FoundItemForm/FoundItemForm';

//define views
const LOST_VIEW = 'This is lost form';
const FOUND_VIEW = 'This is Found form';


const Home = () => {
  

  // use state
  const[activeForm, setActiveForm] = useState(LOST_VIEW);

  //Function
  const renderForm = ()=>{

    if(activeForm == LOST_VIEW){
      return(
        <LostItemForm></LostItemForm>
      )
    }
    if(activeForm == FOUND_VIEW){
      return(
        <FoundItemForm></FoundItemForm>
      )
    }

  }


  return (
    <div className={styles.homeContainer}>
      <div className={styles.card}>
        <h2 className={styles.cardTitle}>Report an Item</h2>
        <div className={styles.buttonGroup}>
          <Button onClick={() => setActiveForm(LOST_VIEW)} variant="lost-submit">
            Report for Lost Item
          </Button>
          <Button onClick={() => setActiveForm(FOUND_VIEW)} variant="found-submit">
            Report for Found Item
          </Button>
        </div>
      </div>

      <div className={styles.infoSection}>

     {/* button er sathe conditional  rendaring hobe. default vabe prothom button button er jonno select hoye thakbe */}
        {renderForm()}

      </div>
    </div>
  );
};

export default Home;