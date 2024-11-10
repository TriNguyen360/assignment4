"use strict";

let app = {};

// Vue app data and methods
app.data = function() {
    return {
        contacts: [], // Stores all contact cards for the current user
        newContact: { // Template for creating a new contact
            name: "",
            affiliation: "",
            description: "",
            photo: "https://bulma.io/assets/images/placeholders/96x96.png"
        }
    };
};

// Methods for handling CRUD operations and image uploads
app.methods = {
    // Load contacts from the server for the current user
    load_data: async function () {
        try {
            let response = await axios.get(get_contacts_url);
            // Initialize contacts and set fields as non-editable initially
            this.contacts = response.data.contacts.map(contact => {
                contact.name_editable = false;
                contact.affiliation_editable = false;
                contact.description_editable = false;
                return contact;
            });
        } catch (error) {
            console.error("Error loading contacts:", error);
        }
    },

    // Add a new contact
    addContact: async function () {
        try {
            let response = await axios.post(add_contact_url);
            if (response.data.contact) {
                let contact = response.data.contact;
                // Set newly added contact's fields as non-editable
                contact.name_editable = false;
                contact.affiliation_editable = false;
                contact.description_editable = false;
                this.contacts.push(contact); // Add the new contact to the list
            }
        } catch (error) {
            console.error("Error adding contact:", error);
        }
    },

    // Delete a contact
    deleteContact: async function (contact_id) {
        try {
            await axios.post(delete_contact_url, { id: contact_id });
            // Filter out the deleted contact from the local state
            this.contacts = this.contacts.filter(contact => contact.id !== contact_id);
        } catch (error) {
            console.error("Error deleting contact:", error);
        }
    },

    // Edit a field in a contact and update it on the server
    editField: async function (contact, field, value) {
        // Make the field read-only after the edit
        contact[`${field}_editable`] = false;
        try {
            let response = await axios.post(update_contact_url, { id: contact.id, field: field, value: value });
            if (response.data.success) {
                contact[field] = value; // Update local contact data with the new value
                console.log(`Successfully saved ${field} for contact ID ${contact.id}`);
            } else {
                console.error(`Failed to update ${field} for contact ID ${contact.id}`);
            }
        } catch (error) {
            console.error("Error updating contact:", error);
        }
    },

    // Trigger file input for image upload when the figure tag is clicked
    choose_image: function (contact) {
        let input = document.getElementById("file-input");
        // Attach an onchange handler to process the selected file
        input.onchange = (event) => {
            this.uploadImage(event, contact);
        };
        input.click(); // Simulate a click on the hidden file input
    },

    // Handle image upload and send it to the server
    uploadImage: async function (event, contact) {
        let file = event.target.files[0];
        if (file) {
            let reader = new FileReader();
            reader.onload = async (e) => {
                let image_data = e.target.result;
                try {
                    let response = await axios.post(upload_image_url, { id: contact.id, image: image_data });
                    if (response.data.success) {
                        // Update the contact's photo with the new image
                        contact.photo = image_data;
                    }
                } catch (error) {
                    console.error("Error uploading image:", error);
                }
            };
            reader.readAsDataURL(file); // Convert image to data URL for upload
        }
    },

    // Allow a field to become editable when clicked
    makeEditable: function (contact, field) {
        contact[`${field}_editable`] = true;
    }
};

// Initialize Vue app
app.vue = Vue.createApp({
    data: app.data,
    methods: app.methods,
    created() {
        this.load_data(); // Load contacts when the app is created
    }
}).mount("#app");
