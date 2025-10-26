import { useState } from 'react';
import styles from './FoundItemForm.module.css';
import InputField from '../../components/InputField/InputField';
import Button from '../../components/Button/Button';

const LostItemForm = () => {
  const [formData, setFormData] = useState({
    itemName: '',
    lostDate: '',
    description: '',
    itemImage: null,
  });

  const handleChange = (e) => {
    const { name, value, type, files } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: type === 'file' ? files[0] : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Lost Item Data:', formData);
    alert('Lost item submitted! (Check console for data)');
    
  };

  return (
    <div className={styles.formContainer}>
      <h2 className={styles.formTitle}>Found item listing</h2>
      <form onSubmit={handleSubmit} className={styles.form}>
        <InputField
          label="Item Name"
          id="itemName"
          name="itemName"
          value={formData.itemName}
          onChange={handleChange}
          placeholder="e.g. Blue backpack"
          required
        />
        <InputField
          label="Lost Date"
          id="lostDate"
          name="lostDate"
          type="date"
          value={formData.lostDate}
          onChange={handleChange}
          required
        />
        <InputField
          label="Description"
          id="description"
          name="description"
          type="textarea"
          value={formData.description}
          onChange={handleChange}
          placeholder="Describe the item, where it was found, etc."
          rows="5"
          required
        />
        <InputField
          label="Upload Item Image"
          id="itemImage"
          name="itemImage"
          type="file"
          onChange={handleChange}
          accept="image/*"
    
        />
        <Button type="submit" variant="found-submit">
          Submit Lost Item
        </Button>
      </form>
    </div>
  );
};

export default LostItemForm;