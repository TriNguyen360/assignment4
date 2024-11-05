"use strict";

let app = {};

// Vue app data and methods
app.data = function() {
    return {
        contacts: [],          // Array to store contact cards
        newContact: {
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
            this.contacts = response.data.contacts; // Load contacts directly from server response
        } catch (error) {
            console.error("Error loading contacts:", error);
        }
    },

    // Add a new contact
    addContact: async function () {
        try {
            let response = await axios.post(add_contact_url);
            if (response.data.contact) {
                this.contacts.push(response.data.contact); // Add the new contact to the list
            }
        } catch (error) {
            console.error("Error adding contact:", error);
        }
    },

    // Delete a contact
    deleteContact: async function (contact_id) {
        try {
            await axios.post(delete_contact_url, { id: contact_id });
            this.contacts = this.contacts.filter(contact => contact.id !== contact_id); // Remove the deleted contact
        } catch (error) {
            console.error("Error deleting contact:", error);
        }
    },

    // Edit a field in a contact and update it on the server
    editField: async function (contact, field, value) {
        try {
            contact[`${field}_editable`] = false; // Set field to read-only on blur
            let response = await axios.post(update_contact_url, { id: contact.id, field: field, value: value });
            if (response.data.success) {
                console.log(`Successfully saved ${field} for contact ID ${contact.id}`);
                // Ensure the contact updates locally without reloading all data
                contact[field] = value;
            } else {
                console.error(`Failed to update ${field} for contact ID ${contact.id}`);
            }
        } catch (error) {
            console.error("Error updating contact:", error);
        }
    },

    // Click handler for figure tag to upload an image
    click_figure: function (contact) {
        let fileInput = document.getElementById(`file-input-${contact.id}`);
        fileInput.click();
    },

    // Handle image upload and send to server
    uploadImage: async function (event, contact) {
        let file = event.target.files[0];
        if (file) {
            let reader = new FileReader();
            reader.onload = async (e) => {
                let image_data = e.target.result;
                try {
                    let response = await axios.post(upload_image_url, { id: contact.id, image: image_data });
                    if (response.data.success) {
                        contact.photo = image_data; // Update the image URL in local state
                    }
                } catch (error) {
                    console.error("Error uploading image:", error);
                }
            };
            reader.readAsDataURL(file);
        }
    },

    // Toggle readonly mode for fields
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
