using UnityEngine;

// Include the namespace required to use Unity UI
using UnityEngine.UI;

using System.Collections;

public class PlayerStats : MonoBehaviour {
	// Create public variables for player speed, and for the Text UI game objects
    private int health = 100;
	private int mana = 100;
	private int healthMax = 100;
	private int manaMax = 100;

	public void ApplyDammage (int TheDammage)
	{
        health -= TheDammage;
        
        if(health <= 0){
            Dead();
			health = 0;
        }
    }

	public void ApplyMana (int Mana)
	{
        mana -= Mana;
        
        if(mana <= 0){
            ManaLeft();
			mana = 0;
        }
    }

	public int getHealth ()
	{
		return(health);
    }

	public int getMana ()
	{
		return(mana);
    }

	public int getHealthMax ()
	{
		return(healthMax);
    }

	public int getManaMax ()
	{
		return(manaMax);
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