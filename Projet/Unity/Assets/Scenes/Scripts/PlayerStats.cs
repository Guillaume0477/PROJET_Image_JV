using UnityEngine;

// Include the namespace required to use Unity UI
using UnityEngine.UI;

using System.Collections;

public class PlayerStats : MonoBehaviour {
	// Create public variables for player speed, and for the Text UI game objects
    private int health = 100;
	private int mana = 100;
	public int manaMax = 100;
	public int healthMax = 100;
	
	// public void set_health(int health){
	// 	this.health = health;
	// }

	// public PlayerStats(int health, int mana)
	// {
	// 	this.health = health;
	// 	this.mana = mana;
	// }

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