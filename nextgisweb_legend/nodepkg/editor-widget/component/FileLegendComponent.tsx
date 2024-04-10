import { observer } from "mobx-react-lite";

import { FileUploader } from "@nextgisweb/file-upload/file-uploader";
import { gettext } from "@nextgisweb/pyramid/i18n";
import type { EditorWidgetProps } from "@nextgisweb/resource/type";

import type { EditorStore } from "../EditorStore";

const msgUploadDescText = gettext("Select a legend description");
const msgHelpDescText = gettext("Only JSON format is supported.");

const msgUploadImageText = gettext("Select a legend image");
const msgHelpImageText = gettext("Only PNG format is supported.");

export const FileLegendComponent = observer(
    ({ store }: EditorWidgetProps<EditorStore>) => {
        return (
            <>
                <FileUploader
                    accept=".png"
                    onChange={(value) => {
                        if (Array.isArray(value)) throw "unreachable";
                        store.setImage(value);
                    }}
                    onUploading={(value) => {
                        store.setUploadingImage(value);
                    }}
                    uploadText={msgUploadImageText}
                    helpText={msgHelpImageText}
                />
                <FileUploader
                    accept=".json"
                    onChange={(value) => {
                        if (Array.isArray(value)) throw "unreachable";
                        store.setDescription(value);
                    }}
                    onUploading={(value) => {
                        store.setUploadingDescription(value);
                    }}
                    uploadText={msgUploadDescText}
                    helpText={msgHelpDescText}
                />
            </>
        );
    }
);
