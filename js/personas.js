// personas.js - Functions for persona management

const API_URL = 'http://127.0.0.1:8000';

// Generate preview audio
async function generatePreviewVoice(text, gender, style, speed) {
    try {
        const response = await fetch(`${API_URL}/preview-voice`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text, gender, style, speed })
        });
        
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Preview error:', error);
        return { success: false, error: error.message };
    }
}

// Save persona to database
async function savePersonaToDB(userId, name, type, gender, style, speed) {
    const { data, error } = await supabase
        .from('personas')
        .insert([{
            user_id: userId,
            name: name,
            type: type,
            gender: gender,
            style: style,
            speed: speed
        }])
        .select();
    
    if (error) throw error;
    return data;
}

// Get user's personas
async function getUserPersonas(userId) {
    const { data, error } = await supabase
        .from('personas')
        .select('*')
        .eq('user_id', userId)
        .order('created_at', { ascending: false });
    
    if (error) throw error;
    return data;
}

// Delete persona
async function deletePersonaFromDB(personaId, userId) {
    const { error } = await supabase
        .from('personas')
        .delete()
        .eq('id', personaId)
        .eq('user_id', userId);
    
    if (error) throw error;
}

// Export functions
window.personasAPI = {
    generatePreviewVoice,
    savePersonaToDB,
    getUserPersonas,
    deletePersonaFromDB
};