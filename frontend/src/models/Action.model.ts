export enum ActionTypes {
    PAUSE = 'PAUSE',
    RESET = 'RESET',
    RESET_ALL = 'RESET_ALL',
    NEXT = 'NEXT',

}

export class Action {
    public constructor(public action: ActionTypes) { };
}