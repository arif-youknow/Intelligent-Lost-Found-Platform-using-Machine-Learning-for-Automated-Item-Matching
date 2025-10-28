import { useState } from 'react';
import styles from './FoundItemForm.module.css';
import InputField from '../../components/InputField/InputField';
import Button from '../../components/Button/Button';
import apiService from "../../Services/ApiServices";


const FoundItemForm = () => {
    
    const [formData, setFormData] = useState({
        
        item_name: '', 
        found_date: '', 
        description: '',     
        item_image: null, 
        itemStatus: 'found'
    });

    const handleChange = (e) => {
        const { name, value, type, files } = e.target;
        setFormData((prevData) => ({
            ...prevData,
            [name]: type === 'file' ? files[0] : value,
        }));
    };

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError(null);
        setSuccess(false);

        const dataToSubmit = new FormData();
        for (const key in formData) {
            if (formData[key] !== null) {
                dataToSubmit.append(key, formData[key]);
            }
        }

        try {
           
            const result = await apiService.submitFoundItem(dataToSubmit);
            console.log('Server Response:', result);
            setSuccess(true);
            
          
            setFormData({
                item_name: '',
                found_date: '', 
                description: '',
                item_image: null, 
                itemStatus: 'found'
            });

        } catch (err) {
            console.error('Error while submitting the form', err);
            
            setError(err.message || 'Error submitting the form');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className={styles.formContainer}>
            <h2 className={styles.formTitle}>Found item listing</h2>
            <form onSubmit={handleSubmit} className={styles.form}>
                <InputField
                    label="Item Name"
                    id="item_name"
                    
                    name="item_name" 
                    value={formData.item_name}
                    onChange={handleChange}
                    placeholder="e.g. Blue backpack"
                    required
                />
                <InputField
                    label="Found Date" 
                    id="found_date"
                    
                    name="found_date" 
                    type="date"
                    value={formData.found_date}
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
                    id="item_image"
                    
                    name="item_image" 
                    type="file"
                    onChange={handleChange}
                    accept="image/*"
                />
                <Button type="submit" variant="found-submit" disabled={loading}>
                    {loading ? 'Please wait..' : 'Submit Found Item'}
                </Button>
                {error && <p style={{ color: 'red' }}>Error: {error}</p>}
                {success && <p style={{ color: 'green' }}>Submitted Successfully!</p>}
            </form>
        </div>
    );
};

export default FoundItemForm;