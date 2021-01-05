using UnityEngine;

// Include the namespace required to use Unity UI
using UnityEngine.UI;

using System.Collections;

public class PlayerStats : MonoBehaviour {
	// Create public variables for player speed, and for the Text UI game objects
    public int healthbase = 100;
	public int healthmax = 100;

	// At the start of the game..
	void ApplyDammage (int TheDammage)
	{
        healthbase -= TheDammage;
        
        if(healthbase <= 0){
            Dead();
        }
    }

	// Each physics step..
	void Dead ()
	{
        Debug.Log("Player died");
	}
}