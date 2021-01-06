using UnityEngine;

// Include the namespace required to use Unity UI
using UnityEngine.UI;

using System.Collections;

public class PlayerStats : MonoBehaviour {
	// Create public variables for player speed, and for the Text UI game objects
    public int healthbase = 100;
	public int healthmax = 100;
	public int mana = 100;

	void ApplyDammage (int TheDammage)
	{
        healthbase -= TheDammage;
        
        if(healthbase <= 0){
            Dead();
        }
    }

	void ApplyMana (int Mana)
	{
        mana -= Mana;
        
        if(mana <= 0){
            ManaLeft();
        }
    }

	void Dead ()
	{
        Debug.Log("Player died !");
	}

	// Each physics step..
	void ManaLeft ()
	{
        Debug.Log("No more mana !");
	}
}