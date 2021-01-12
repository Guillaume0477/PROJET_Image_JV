using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class CommandsMenu : MonoBehaviour
{
    // public Dropdown commandsDropDown;

    // public void Start()
    // {
    //     // commandsDropDown.ClearOptions();

    //     // commandsDropDown.AddOptions(new List<Dropdown.OptionData> {
    //     // new Dropdown.OptionData {text="Initial position", 
    //     // image=Resources.Load("../data/ImagesExample/Capture d’écran 2021-01-11 à 11.13.20", typeof(Sprite)) 
    //     // as Sprite}
    //     // });
    // }

    public void GoBackCommands()
    {
        gameObject.SetActive(false);
    }
}
